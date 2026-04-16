#pragma once

#include <cstdint>

class Interrupts;

class Timer {
    Interrupts *interrupts;

    uint16_t counter = 0;
    uint8_t tima = 0;
    uint8_t tma = 0;
    uint8_t tac = 0;

    bool last_tick_input = false;
    bool overflow_pending = false;
    bool just_reloaded = false;

    static constexpr int COUNTER_BIT_BY_CLOCK[4] = {9, 3, 5, 7};

    void step_m_cycle();
    void detect_falling_edge();
    bool get_tick_input() const;

   public:
    Timer(Interrupts *interrupts);

    void tick(int tcycles);

    uint8_t read_div() const;
    void write_div();

    uint8_t read_tima() const;
    void write_tima(uint8_t value);

    uint8_t read_tma() const;
    void write_tma(uint8_t value);

    uint8_t read_tac() const;
    void write_tac(uint8_t value);

    void set_counter(uint16_t value);
};
