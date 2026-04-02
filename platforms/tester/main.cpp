#include "gb.h"

#include <cstdlib>
#include <iostream>
#include <getopt.h>
#include <unistd.h>

// Mooneye pass: Fibonacci sequence in registers
static bool check_mooneye_pass(Registers &regs) {
    return regs.b == 3 && regs.c == 5 && regs.d == 8 &&
           regs.e == 13 && regs.h == 21 && regs.l == 34;
}

static bool check_mooneye_fail(Registers &regs) {
    return regs.b == 0x42 && regs.c == 0x42 && regs.d == 0x42 &&
           regs.e == 0x42 && regs.h == 0x42 && regs.l == 0x42;
}

static int run_headless(const std::string &rom, long long max_cycles, const std::string &detection) {
    Cartridge *cartridge = new Cartridge(rom);
    MMU *mmu = new MMU(cartridge);
    Registers registers;
    Interrupts *interrupts = new Interrupts(&registers, mmu);
    CPU *cpu = new CPU(&registers, interrupts, mmu);
    PPU *ppu = new PPU(&registers, interrupts, mmu);
    Timer *timer = new Timer(mmu, interrupts);

    // Post-bootrom initialization
    cpu->no_bootrom_init();

    long long total_cycles = 0;
    int result = 2;  // timeout by default
    size_t last_serial_len = 0;

    while (total_cycles < max_cycles) {
        // Check Mooneye LD B,B breakpoint (opcode 0x40)
        if (detection != "serial" && registers.pc >= 0x0100) {
            uint8_t next_op = mmu->read_byte(registers.pc);
            if (next_op == 0x40) {
                if (check_mooneye_pass(registers)) { result = 0; break; }
                if (check_mooneye_fail(registers)) { result = 1; break; }
            }
        }

        // Check serial output for Blargg results (only when buffer grows)
        if (detection != "mooneye" && mmu->serial_output.size() > last_serial_len) {
            last_serial_len = mmu->serial_output.size();
            if (mmu->serial_output.find("Passed") != std::string::npos) { result = 0; break; }
            if (mmu->serial_output.find("Failed") != std::string::npos) { result = 1; break; }
        }

        // Execute one step
        mmu->clock.t_instr = 0;
        bool interrupted = interrupts->check();
        if (!interrupted) cpu->step();
        timer->inc();
        ppu->step();
        total_cycles += mmu->clock.t_instr;
    }

    // Output results
    if (!mmu->serial_output.empty())
        std::cout << "SERIAL:" << mmu->serial_output << std::endl;

    if (result == 0)
        std::cout << "RESULT:PASS" << std::endl;
    else if (result == 1)
        std::cout << "RESULT:FAIL" << std::endl;
    else
        std::cout << "RESULT:TIMEOUT" << std::endl;

    delete timer;
    delete ppu;
    delete cpu;
    delete interrupts;
    delete mmu;
    delete cartridge;
    return result;
}

int main(int argc, char *argv[]) {
    std::string rom = "";
    std::string detection = "auto";
    long long timeout_cycles = 100000000;
    
    // We ignore headless flag because this program is inherently headless.
    int headless_flag = 0; 

    static struct option long_options[] = {
        {"headless", no_argument, &headless_flag, true},
        {"rom", required_argument, 0, 'r'},
        {"timeout", required_argument, 0, 't'},
        {"detection", required_argument, 0, 'd'},
        {0, 0, 0, 0}
    };

    int opt;
    int option_index = 0;
    while ((opt = getopt_long(argc, argv, "r:t:d:", long_options, &option_index)) != EOF) {
        if (-1 == opt)
            break;
        switch (opt) {
            case 0:
                break;
            case 'r':
                rom = std::string(optarg);
                if (access(rom.c_str(), F_OK) == -1) {
                    std::cout << "The rom file doesn't exist" << std::endl;
                    exit(1);
                }
                break;
            case 't':
                timeout_cycles = std::atoll(optarg);
                break;
            case 'd':
                detection = std::string(optarg);
                break;
            default:
                abort();
        }
    }
    if (rom.empty()) {
        std::cout << "Missing rom argument" << std::endl;
        exit(1);
    }

    return run_headless(rom, timeout_cycles, detection);
}
