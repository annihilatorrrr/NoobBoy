#include "gb.h"

#include <cstdlib>
#include <iostream>
#include <getopt.h>
#include <unistd.h>

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

static int run_headless(const std::string &rom, long long max_cycles, const std::string &detection) {
    GB gb;
    gb.init(rom, true, "", "", false, false, true);

    long long total_cycles = 0;
    int result = 2;  // timeout by default
    size_t last_serial_len = 0;

    while (total_cycles < max_cycles) {
        // Check Mooneye LD B,B breakpoint (opcode 0x40) before executing
        if (detection != "serial" && gb.registers.pc >= 0x0100) {
            uint8_t next_op = gb.mmu->memory[gb.registers.pc];
            if (gb.registers.pc < 0x8000)
                next_op = gb.mmu->cartridge->mbc_read(gb.registers.pc);
            if (next_op == 0x40) {
                if (check_mooneye_pass(gb.registers)) {
                    result = 0;
                    break;
                }
                if (check_mooneye_fail(gb.registers)) {
                    result = 1;
                    break;
                }
            }
        }

        // Execute one step using the same path as the desktop target
        gb.run_step();
        total_cycles += gb.mmu->clock.t_instr;

        // Check serial output for Blargg results (only when buffer grows)
        if (detection != "mooneye" && gb.mmu->serial_output.size() > last_serial_len) {
            last_serial_len = gb.mmu->serial_output.size();
            if (gb.mmu->serial_output.find("Passed") != std::string::npos) {
                result = 0;
                break;
            }
            if (gb.mmu->serial_output.find("Failed") != std::string::npos) {
                result = 1;
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
                    result = 0;
                    break;
                } else if (status_byte != 0x80) {
                    result = 1;
                    break;
                }
            }
        }
    }

    // Output serial data
    if (!gb.mmu->serial_output.empty())
        std::cout << "SERIAL:" << gb.mmu->serial_output << std::endl;

    // For memory-based tests, also output the text result from cartridge RAM
    if (detection == "memory") {
        std::string mem_text = read_memory_string(gb.mmu, 0xA004, 256);
        if (!mem_text.empty())
            std::cout << "SERIAL:" << mem_text << std::endl;
    }

    if (result == 0)
        std::cout << "RESULT:PASS" << std::endl;
    else if (result == 1)
        std::cout << "RESULT:FAIL" << std::endl;
    else
        std::cout << "RESULT:TIMEOUT" << std::endl;

    return result;
}

int main(int argc, char *argv[]) {
    std::string rom;
    std::string detection = "auto";
    long long timeout_cycles = 100000000;
    int headless_flag = 0;

    static struct option long_options[] = {
        {"headless", no_argument, &headless_flag, 1},
        {"rom", required_argument, 0, 'r'},
        {"timeout", required_argument, 0, 't'},
        {"detection", required_argument, 0, 'd'},
        {0, 0, 0, 0},
    };

    int opt;
    int option_index = 0;
    while ((opt = getopt_long(argc, argv, "r:t:d:", long_options, &option_index)) != EOF) {
        if (opt == -1) break;
        switch (opt) {
            case 0:
                break;
            case 'r':
                rom = std::string(optarg);
                if (access(rom.c_str(), F_OK) == -1) {
                    std::cerr << "The rom file doesn't exist" << std::endl;
                    return 1;
                }
                break;
            case 't':
                timeout_cycles = std::atoll(optarg);
                break;
            case 'd':
                detection = std::string(optarg);
                break;
            default:
                return 1;
        }
    }

    if (rom.empty()) {
        std::cerr << "Missing rom argument" << std::endl;
        return 1;
    }

    return run_headless(rom, timeout_cycles, detection);
}
