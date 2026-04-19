// #include <cstring>
#include "cpu.h"
#include "ppu.h"
#include "apu.h"
#include "timer.h"
#include "renderer.h"
#include "cartridge.h"
#include "interrupt.h"
#include "joypad.h"
#include "status.h"
#include "registers.h"
#include "mmu.h"

#include <iostream>
#include <cstdint>
#include <unistd.h>
#include <set>
#include <chrono>
#include <thread>
#include <getopt.h>

class GB {
   public:
    Status status;

    Registers registers;
    MMU *mmu = nullptr;
    CPU *cpu = nullptr;
    PPU *ppu = nullptr;
    APU *apu = nullptr;
    Interrupts *interrupts = nullptr;
    Timer *timer = nullptr;
    Renderer *renderer = nullptr;
    Joypad *joypad = nullptr;
    Cartridge *cartridge = nullptr;
    
    // TODO: Remove the headless parameter
    void init(std::string rom, bool no_bootrom = false, std::string bootrom = "", std::string save_file = "",
              bool debug = false, bool sound = false, bool headless = false);
    void init(Cartridge *cartridge, bool no_bootrom = false, std::string bootrom = "", bool debug = false,
              bool sound = false, bool headless = false);
    bool run_step();
    void run();
    void run_until_next_frame();
};
