#include "gb.h"

#include <chrono>
#include <cstdlib>
#include <getopt.h>
#include <iostream>
#include <unistd.h>

// Exit codes
static constexpr int EXIT_PASS = 0;
static constexpr int EXIT_FAIL = 1;
static constexpr int EXIT_TIMEOUT = 2;
static constexpr int EXIT_HANG = 3;
static constexpr int EXIT_ERROR = 4;

static bool check_mooneye_pass(Registers &regs) {
    return regs.b == 3 && regs.c == 5 && regs.d == 8 && regs.e == 13 && regs.h == 21 && regs.l == 34;
}

static bool check_mooneye_fail(Registers &regs) {
    return regs.b == 0x42 && regs.c == 0x42 && regs.d == 0x42 && regs.e == 0x42 && regs.h == 0x42 &&
           regs.l == 0x42;
}

static std::string read_memory_string(MMU *mmu, uint16_t start, int max_len) {
    std::string out;
    for (int i = 0; i < max_len; i++) {
        uint8_t ch = mmu->cartridge->mbc_read(start + i);
        if (ch == 0) break;
        out += static_cast<char>(ch);
    }
    return out;
}

// Check for the mooneye canonical canary: LD B,B (0x40) at pc.
// Mooneye sets registers to Fibonacci (3,5,8,13,21,34) for pass or 0x42×6 for fail before executing LD B,B.
static bool is_mooneye_breakpoint(MMU *mmu, uint16_t pc) { return mmu->read_byte(pc, false) == 0x40; }

static int run_headless(const std::string &rom, long long max_cycles, const std::string &detection,
                        int max_wall_seconds) {
    GB gb;
    gb.init(rom, true, "", "", false, false, true);

    long long total_cycles = 0;
    int result = EXIT_TIMEOUT;  // timeout by default

    // Stagnation detection state
    uint16_t last_pc = 0xFFFF;
    long long last_progress_cycles = 0;
    static constexpr int STAGNATION_THRESHOLD = 1000000;
    int stagnation_steps = 0;

    // Wall-clock safety valve
    auto wall_start = std::chrono::steady_clock::now();

    while (total_cycles < max_cycles) {
        // Wall-clock hang detection
        auto now = std::chrono::steady_clock::now();
        int elapsed_seconds = std::chrono::duration_cast<std::chrono::seconds>(now - wall_start).count();
        if (max_wall_seconds > 0 && elapsed_seconds >= max_wall_seconds) {
            result = EXIT_HANG;
            break;
        }

        // Check Mooneye LD B,B breakpoint before executing
        if (detection != "serial" && gb.registers.pc >= 0x0100) {
            if (is_mooneye_breakpoint(gb.mmu, gb.registers.pc)) {
                if (check_mooneye_pass(gb.registers)) {
                    result = EXIT_PASS;
                    break;
                }
                if (check_mooneye_fail(gb.registers)) {
                    result = EXIT_FAIL;
                    break;
                }
            }
        }

        // Execute one step
        uint16_t pc_before = gb.registers.pc;
        gb.run_step();
        total_cycles += gb.mmu->clock.t_instr;

        // Stagnation detection: track if PC hasn't changed
        if (gb.registers.pc == pc_before && gb.mmu->clock.t_instr == 0) {
            stagnation_steps++;
            if (stagnation_steps >= STAGNATION_THRESHOLD) {
                result = EXIT_HANG;
                break;
            }
        } else {
            stagnation_steps = 0;
        }

        // Check serial output for Blargg results
        if (detection != "mooneye" && gb.mmu->serial_output.size() > 0) {
            if (gb.mmu->serial_output.find("Passed") != std::string::npos) {
                result = EXIT_PASS;
                break;
            }
            if (gb.mmu->serial_output.find("Failed") != std::string::npos) {
                result = EXIT_FAIL;
                break;
            }
        }

        // Check $A000 cartridge RAM for blargg memory-based results
        if (detection == "memory") {
            uint8_t sig1 = gb.mmu->cartridge->mbc_read(0xA001);
            uint8_t sig2 = gb.mmu->cartridge->mbc_read(0xA002);
            uint8_t sig3 = gb.mmu->cartridge->mbc_read(0xA003);
            if (sig1 == 0xDE && sig2 == 0xB0 && sig3 == 0x61) {
                uint8_t status_byte = gb.mmu->cartridge->mbc_read(0xA000);
                if (status_byte == 0x00) {
                    result = EXIT_PASS;
                    break;
                } else if (status_byte != 0x80) {
                    result = EXIT_FAIL;
                    break;
                }
            }
        }
    }

    // Output serial data only if non-empty
    if (!gb.mmu->serial_output.empty())
        std::cout << "SERIAL:" << gb.mmu->serial_output << std::endl;

    // For memory-based tests, also output the text result from cartridge RAM
    if (detection == "memory") {
        std::string mem_text = read_memory_string(gb.mmu, 0xA004, 256);
        if (!mem_text.empty())
            std::cout << "SERIAL:" << mem_text << std::endl;
    }

    if (result == EXIT_PASS)
        std::cout << "RESULT:PASS" << std::endl;
    else if (result == EXIT_FAIL)
        std::cout << "RESULT:FAIL" << std::endl;
    else if (result == EXIT_HANG)
        std::cout << "RESULT:HANG" << std::endl;
    else
        std::cout << "RESULT:TIMEOUT" << std::endl;

    return result;
}

int main(int argc, char *argv[]) {
    std::string rom;
    std::string detection = "auto";
    long long timeout_cycles = 100000000;
    int max_wall_seconds = 30;
    int headless_flag = 0;

    static struct option long_options[] = {
        {"headless", no_argument, &headless_flag, 1},
        {"rom", required_argument, 0, 'r'},
        {"timeout", required_argument, 0, 't'},
        {"detection", required_argument, 0, 'd'},
        {"max-wall-seconds", required_argument, 0, 'w'},
        {0, 0, 0, 0},
    };

    int opt;
    int option_index = 0;
    while ((opt = getopt_long(argc, argv, "r:t:d:w:", long_options, &option_index)) != EOF) {
        if (opt == -1) break;
        switch (opt) {
            case 0:
                break;
            case 'r':
                rom = std::string(optarg);
                if (access(rom.c_str(), F_OK) == -1) {
                    std::cerr << "The rom file doesn't exist" << std::endl;
                    return EXIT_ERROR;
                }
                break;
            case 't':
                timeout_cycles = std::atoll(optarg);
                break;
            case 'd':
                detection = std::string(optarg);
                break;
            case 'w':
                max_wall_seconds = std::atoi(optarg);
                break;
            default:
                return EXIT_ERROR;
        }
    }

    if (rom.empty()) {
        std::cerr << "Missing rom argument" << std::endl;
        return EXIT_ERROR;
    }

    try {
        return run_headless(rom, timeout_cycles, detection, max_wall_seconds);
    } catch (const std::exception &e) {
        std::cerr << "Internal error: " << e.what() << std::endl;
        return EXIT_ERROR;
    } catch (...) {
        std::cerr << "Unknown internal error" << std::endl;
        return EXIT_ERROR;
    }
}
