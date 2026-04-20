# NoobBoy — Test Results

> Generated on 2026-04-20 11:33:37

**70** of **236** runnable tests passing (30%) — 55 skipped

| | Count |
|:--|--:|
| <span style="color:green">Passed</span> | 70 |
| <span style="color:red">Failed</span> | 75 |
| <span style="color:goldenrod">Timeout</span> | 90 |
| <span style="color:goldenrod">Hang</span> | 0 |
| <span style="color:red">Crashed</span> | 1 |
| <span style="color:red">Error</span> | 0 |
| <span style="color:gray">Skipped</span> | 55 |
| **Total** | **291** |

---

## <span style="color:gray">acid</span> — Skipped

*GBC ROM (DMG only)*
*Visual comparison required*

---

## ax6 — <span style="color:red">0/3</span>

### General — <span style="color:red">0/3</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | rtc3test-1.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | rtc3test-2.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | rtc3test-3.gb | <span style="color:goldenrod">Timeout</span> |  |

---

## blargg — <span style="color:goldenrod">18/39</span>

### General — <span style="color:goldenrod">1/2</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | instr_timing.gb | <span style="color:green">Pass</span> | instr_timing |
| <span style="color:orangered">!</span> | interrupt_time.gb | <span style="color:orangered">**CRASH**</span> |  |

### cgb_sound — <span style="color:red">0/12</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | 01-registers.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 02-len_ctr.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 03-trigger.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 04-sweep.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 05-sweep_details.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 06-overflow_on_trigger.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 07-len_sweep_period_sync.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 08-len_ctr_during_power.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 09-wave_read_while_on.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 10-wave_trigger_while_on.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 11-regs_after_power.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 12-wave.gb | <span style="color:goldenrod">Timeout</span> |  |

### cpu_instrs — <span style="color:green">11/11</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | 01-special.gb | <span style="color:green">Pass</span> | 01-special |
| <span style="color:green">✓</span> | 02-interrupts.gb | <span style="color:green">Pass</span> | 02-interrupts |
| <span style="color:green">✓</span> | 03-op_sp,hl.gb | <span style="color:green">Pass</span> | 03-op sp,hl |
| <span style="color:green">✓</span> | 04-op_r,imm.gb | <span style="color:green">Pass</span> | 04-op r,imm |
| <span style="color:green">✓</span> | 05-op_rp.gb | <span style="color:green">Pass</span> | 05-op rp |
| <span style="color:green">✓</span> | 06-ld_r,r.gb | <span style="color:green">Pass</span> | 06-ld r,r |
| <span style="color:green">✓</span> | 07-jr,jp,call,ret,rst.gb | <span style="color:green">Pass</span> | 07-jr,jp,call,ret,rst |
| <span style="color:green">✓</span> | 08-misc_instrs.gb | <span style="color:green">Pass</span> | 08-misc instrs |
| <span style="color:green">✓</span> | 09-op_r,r.gb | <span style="color:green">Pass</span> | 09-op r,r |
| <span style="color:green">✓</span> | 10-bit_ops.gb | <span style="color:green">Pass</span> | 10-bit ops |
| <span style="color:green">✓</span> | 11-op_a,(hl).gb | <span style="color:green">Pass</span> | 11-op a,(hl) |

### <span style="color:gray">dmg_sound</span> — Skipped

*Instruction timing not yet accurate*

### mem_timing — <span style="color:green">3/3</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | 01-read_timing.gb | <span style="color:green">Pass</span> | 01-read_timing |
| <span style="color:green">✓</span> | 02-write_timing.gb | <span style="color:green">Pass</span> | 02-write_timing |
| <span style="color:green">✓</span> | 03-modify_timing.gb | <span style="color:green">Pass</span> | 03-modify_timing |

### mem_timing-2 — <span style="color:green">3/3</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | 01-read_timing.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | 02-write_timing.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | 03-modify_timing.gb | <span style="color:green">Pass</span> |  |

### oam_bug — <span style="color:red">0/8</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | 1-lcd_sync.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 2-causes.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 3-non_causes.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 4-scanline_timing.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 5-timing_bug.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 6-timing_no_bug.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 7-timing_effect.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | 8-instr_effect.gb | <span style="color:goldenrod">Timeout</span> |  |

---

## cpp — <span style="color:red">0/3</span>

### General — <span style="color:red">0/3</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | latch-rtc-test.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | ramg-mbc3-test.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | rtc-invalid-banks-test.gb | <span style="color:goldenrod">Timeout</span> |  |

---

## daid — <span style="color:red">0/4</span>

### General — <span style="color:red">0/4</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | ppu_scanline_bgp.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | rom_and_ram.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | stop_instr.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | stop_instr_gbc_mode3.gb | <span style="color:goldenrod">Timeout</span> |  |

---

## <span style="color:gray">hacktix</span> — Skipped

*Visual comparison required*

---

## <span style="color:gray">mealybug-tearoom-tests</span> — Skipped

*Visual comparison required*

---

## mooneye — <span style="color:goldenrod">51/111</span>

### acceptance — <span style="color:goldenrod">5/41</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | add_sp_e_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_div-S.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_div-dmg0.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_div-dmgABCmgb.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_div2-S.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_hwio-S.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_hwio-dmg0.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_hwio-dmgABCmgb.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_regs-dmg0.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:green">✓</span> | boot_regs-dmgABC.gb | <span style="color:green">Pass</span> |  |
| <span style="color:goldenrod">T</span> | boot_regs-mgb.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_regs-sgb.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_regs-sgb2.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | call_cc_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | call_cc_timing2.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | call_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | call_timing2.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | di_timing-GS.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:green">✓</span> | div_timing.gb | <span style="color:green">Pass</span> |  |
| <span style="color:goldenrod">T</span> | ei_sequence.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | ei_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:green">✓</span> | halt_ime0_ei.gb | <span style="color:green">Pass</span> |  |
| <span style="color:goldenrod">T</span> | halt_ime0_nointr_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:green">✓</span> | halt_ime1_timing.gb | <span style="color:green">Pass</span> |  |
| <span style="color:goldenrod">T</span> | halt_ime1_timing2-GS.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | if_ie_registers.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | intr_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | jp_cc_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | jp_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | ld_hl_sp_e_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | oam_dma_restart.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | oam_dma_start.gb | <span style="color:goldenrod">Timeout</span> |  |
| <span style="color:goldenrod">T</span> | oam_dma_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:green">✓</span> | pop_timing.gb | <span style="color:green">Pass</span> |  |
| <span style="color:goldenrod">T</span> | push_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | rapid_di_ei.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | ret_cc_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | ret_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | reti_intr_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | reti_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | rst_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |

### acceptance/bits — <span style="color:goldenrod">1/2</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | mem_oam.gb | <span style="color:green">Pass</span> |  |
| <span style="color:goldenrod">T</span> | unused_hwio-GS.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |

### acceptance/instr — <span style="color:green">1/1</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | daa.gb | <span style="color:green">Pass</span> |  |

### acceptance/interrupts — <span style="color:red">0/1</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | ie_push.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |

### acceptance/oam_dma — <span style="color:goldenrod">2/3</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | basic.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | reg_read.gb | <span style="color:green">Pass</span> |  |
| <span style="color:goldenrod">T</span> | sources-GS.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |

### acceptance/ppu — <span style="color:goldenrod">1/12</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | hblank_ly_scx_timing-GS.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | intr_1_2_timing-GS.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:green">✓</span> | intr_2_0_timing.gb | <span style="color:green">Pass</span> |  |
| <span style="color:goldenrod">T</span> | intr_2_mode0_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | intr_2_mode0_timing_sprites.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | intr_2_mode3_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | intr_2_oam_ok_timing.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | lcdon_timing-GS.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | lcdon_write_timing-GS.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | stat_irq_blocking.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | stat_lyc_onoff.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | vblank_stat_intr-GS.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |

### acceptance/serial — <span style="color:red">0/1</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | boot_sclk_align-dmgABCmgb.gb | <span style="color:goldenrod">Timeout</span> | \x00BBBBBB |

### acceptance/timer — <span style="color:green">13/13</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | div_write.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rapid_toggle.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tim00.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tim00_div_trigger.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tim01.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tim01_div_trigger.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tim10.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tim10_div_trigger.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tim11.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tim11_div_trigger.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tima_reload.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tima_write_reloading.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | tma_write_reloading.gb | <span style="color:green">Pass</span> |  |

### emulator-only/mbc1 — <span style="color:green">13/13</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | bits_bank1.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | bits_bank2.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | bits_mode.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | bits_ramg.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | multicart_rom_8Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | ram_256kb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | ram_64kb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_16Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_1Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_2Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_4Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_512kb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_8Mb.gb | <span style="color:green">Pass</span> |  |

### emulator-only/mbc2 — <span style="color:green">7/7</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | bits_ramg.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | bits_romb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | bits_unused.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | ram.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_1Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_2Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_512kb.gb | <span style="color:green">Pass</span> |  |

### emulator-only/mbc5 — <span style="color:green">8/8</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:green">✓</span> | rom_16Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_1Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_2Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_32Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_4Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_512kb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_64Mb.gb | <span style="color:green">Pass</span> |  |
| <span style="color:green">✓</span> | rom_8Mb.gb | <span style="color:green">Pass</span> |  |

### manual-only — <span style="color:red">0/1</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | sprite_priority.gb | <span style="color:goldenrod">Timeout</span> |  |

### misc — <span style="color:red">0/6</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | boot_div-A.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_div-cgb0.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_div-cgbABCDE.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_hwio-C.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_regs-A.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |
| <span style="color:goldenrod">T</span> | boot_regs-cgb.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |

### misc/bits — <span style="color:red">0/1</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | unused_hwio-C.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |

### misc/ppu — <span style="color:red">0/1</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:goldenrod">T</span> | vblank_stat_intr-C.gb | <span style="color:goldenrod">Timeout</span> | BBBBBB |

---

## samesuite — <span style="color:goldenrod">1/76</span>

### apu — <span style="color:red">0/5</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:orangered">✗</span> | div_trigger_volume_10.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | div_write_trigger.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | div_write_trigger_10.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | div_write_trigger_volume.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | div_write_trigger_volume_10.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |

### apu/channel_1 — <span style="color:red">0/21</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:orangered">✗</span> | channel_1_align.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_align_cpu.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_duty.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_duty_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_extra_length_clocking-cgb0B.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_freq_change.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_freq_change_timing-A.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_freq_change_timing-cgb0BC.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_freq_change_timing-cgbDE.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_nrx2_glitch.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_nrx2_speed_change.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_restart.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_restart_nrx2_glitch.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_stop_div.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_stop_restart.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_sweep.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_sweep_restart.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_sweep_restart_2.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_volume.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_1_volume_div.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |

### apu/channel_2 — <span style="color:red">0/15</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:orangered">✗</span> | channel_2_align.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_align_cpu.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_duty.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_duty_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_extra_length_clocking-cgb0B.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_freq_change.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_nrx2_glitch.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_nrx2_speed_change.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_restart.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_restart_nrx2_glitch.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_stop_div.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_stop_restart.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_volume.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_2_volume_div.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |

### apu/channel_3 — <span style="color:goldenrod">1/15</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:orangered">✗</span> | channel_3_and_glitch.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_extra_length_clocking-cgb0.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_extra_length_clocking-cgbB.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_first_sample.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_freq_change_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_restart_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_restart_during_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_restart_stop_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_shift_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_shift_skip_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:green">✓</span> | channel_3_stop_delay.gb | <span style="color:green">Pass</span> | \x03\x05\x08 |
| <span style="color:orangered">✗</span> | channel_3_stop_div.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_wave_ram_locked_write.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_3_wave_ram_sync.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |

### apu/channel_4 — <span style="color:red">0/13</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:orangered">✗</span> | channel_4_align.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_delay.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_equivalent_frequencies.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_extra_length_clocking-cgb0B.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_freq_change.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_frequency_alignment.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_lfsr.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_lfsr15.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_lfsr_15_7.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_lfsr_7_15.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_lfsr_restart.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_lfsr_restart_fast.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | channel_4_volume_div.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |

### dma — <span style="color:red">0/4</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:orangered">✗</span> | gbc_dma_cont.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | gdma_addr_mask.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | hdma_lcd_off.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | hdma_mode0.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |

### ppu — <span style="color:red">0/1</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:orangered">✗</span> | blocking_bgpi_increase.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |

### sgb — <span style="color:red">0/2</span>

| | Test | Status | Output |
|:--|:--|:--|:--|
| <span style="color:orangered">✗</span> | command_mlt_req.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |
| <span style="color:orangered">✗</span> | command_mlt_req_1_incrementing.gb | <span style="color:orangered">**FAIL**</span> | BBBBBB |

