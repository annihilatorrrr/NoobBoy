#include "gb.h"

void GB::init(std::string rom, bool no_bootrom, std::string bootrom, std::string save_file, bool debug, bool sound,
              bool headless) {
    Cartridge *cartridge = new Cartridge(rom, save_file);
    this->init(cartridge, no_bootrom, bootrom, debug, sound, headless);
}

void GB::init(Cartridge *cartridge, bool no_bootrom, std::string bootrom, bool debug, bool sound, bool headless) {
    this->cartridge = cartridge;
    mmu = new MMU(cartridge);

    interrupts = new Interrupts(&registers, mmu);
    timer = new Timer(interrupts);
    cpu = new CPU(&registers, interrupts, timer, mmu);
    ppu = new PPU(&registers, interrupts, mmu);
    mmu->timer = timer;
    apu = new APU(&status, mmu, !sound || headless);
    status.debug = debug;

    if (!headless) {
        joypad = new Joypad(&status, interrupts, mmu);

        if (debug)
            renderer = new DebugRenderer(&status, cpu, ppu, &registers, interrupts, mmu);
        else
            renderer = new Renderer(&status, cpu, ppu, &registers, interrupts, mmu);
        renderer->init();
    }

    if (no_bootrom)
        cpu->no_bootrom_init();
    else if (!bootrom.empty())
        mmu->load_boot_rom(bootrom);
    else
        mmu->load_default_boot_rom();

    status.isRunning = true;
}

bool GB::run_step() {
    mmu->clock.t_instr = 0;

    if (!status.isPaused || status.doStep) {
        bool interrupted = interrupts->check();
        if (!interrupted)
            cpu->step();
        ppu->step();
    }

    status.doStep = false;

    if (joypad)
        joypad->check(mmu->clock.t_instr);

    if (renderer && (ppu->can_render || status.isPaused)) {
        renderer->render();
        ppu->can_render = false;
        return true;
    }
    return false;
}

void GB::run() {
    while (status.isRunning) {
        this->run_step();
    }
}

void GB::run_until_next_frame() {
    while (!this->run_step()) {
    }
}
