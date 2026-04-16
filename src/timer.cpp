#include "timer.h"
#include "interrupt.h"

Timer::Timer(Interrupts* interrupts) : interrupts(interrupts) {}

void Timer::tick(int tcycles) {
    just_reloaded = false;
    for (int i = 0; i < tcycles; i += 4) {
        step_m_cycle();
    }
}

void Timer::step_m_cycle() {
    if (overflow_pending) {
        tima = tma;
        interrupts->set_interrupt_flag(INTERRUPT_TIMER);
        overflow_pending = false;
        just_reloaded = true;
    }

    counter += 4;
    detect_falling_edge();
}

bool Timer::get_tick_input() const {
    int bit = COUNTER_BIT_BY_CLOCK[tac & 0x03];
    bool timer_enabled = (tac >> 2) & 1;
    return ((counter >> bit) & 1) && timer_enabled;
}

void Timer::detect_falling_edge() {
    bool current = get_tick_input();

    if (last_tick_input && !current) {
        tima++;
        if (tima == 0) {
            overflow_pending = true;
        }
    }

    last_tick_input = current;
}

uint8_t Timer::read_div() const {
    return counter >> 8;
}

void Timer::write_div() {
    counter = 0;
    detect_falling_edge();
}

uint8_t Timer::read_tima() const {
    return tima;
}

void Timer::write_tima(uint8_t value) {
    if (just_reloaded)
        return;

    if (overflow_pending)
        overflow_pending = false;

    tima = value;
}

uint8_t Timer::read_tma() const {
    return tma;
}

void Timer::write_tma(uint8_t value) {
    if (just_reloaded)
        tima = value;

    tma = value;
}

uint8_t Timer::read_tac() const {
    return tac;
}

void Timer::write_tac(uint8_t value) {
    tac = value;
    detect_falling_edge();
}

void Timer::set_counter(uint16_t value) {
    counter = value;
    last_tick_input = get_tick_input();
}
