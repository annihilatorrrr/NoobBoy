# NoobBoy — Test Results

> Generated on 2026-04-16 10:06:29

**64** of **250** runnable tests passing (26%)
 · 41 skipped

| | Count |
|---|--:|
| Passed | 64 |
| Failed | 0 |
| Timeout | 107 |
| Crashed | 79 |
| Skipped | 41 |
| **Total** | **291** |

---

## acid

### General

*GBC ROM (DMG only)*

---

## ax6

### General — 0/3 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| rtc3test-1.gb | ⏱ |
| rtc3test-2.gb | ⏱ |
| rtc3test-3.gb | ⏱ |

</details>

---

## blargg

### General — 1/3 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| halt_bug.gb | 💥 |
| instr_timing.gb | ✅ |
| interrupt_time.gb | 💥 |

</details>

### cgb_sound — 0/12 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| 01-registers.gb | ⏱ |
| 02-len_ctr.gb | ⏱ |
| 03-trigger.gb | ⏱ |
| 04-sweep.gb | ⏱ |
| 05-sweep_details.gb | ⏱ |
| 06-overflow_on_trigger.gb | ⏱ |
| 07-len_sweep_period_sync.gb | ⏱ |
| 08-len_ctr_during_power.gb | ⏱ |
| 09-wave_read_while_on.gb | ⏱ |
| 10-wave_trigger_while_on.gb | ⏱ |
| 11-regs_after_power.gb | ⏱ |
| 12-wave.gb | ⏱ |

</details>

### cpu_instrs — 11/11 ✅

All tests passing.

### dmg_sound — 0/12 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| 01-registers.gb | ⏱ |
| 02-len_ctr.gb | ⏱ |
| 03-trigger.gb | ⏱ |
| 04-sweep.gb | ⏱ |
| 05-sweep_details.gb | ⏱ |
| 06-overflow_on_trigger.gb | ⏱ |
| 07-len_sweep_period_sync.gb | ⏱ |
| 08-len_ctr_during_power.gb | ⏱ |
| 09-wave_read_while_on.gb | ⏱ |
| 10-wave_trigger_while_on.gb | ⏱ |
| 11-regs_after_power.gb | ⏱ |
| 12-wave_write_while_on.gb | ⏱ |

</details>

### mem_timing — 0/3 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| 01-read_timing.gb | 💥 |
| 02-write_timing.gb | 💥 |
| 03-modify_timing.gb | 💥 |

</details>

### mem_timing-2 — 0/3 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| 01-read_timing.gb | ⏱ |
| 02-write_timing.gb | ⏱ |
| 03-modify_timing.gb | ⏱ |

</details>

### oam_bug — 0/8 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| 1-lcd_sync.gb | ⏱ |
| 2-causes.gb | ⏱ |
| 3-non_causes.gb | ⏱ |
| 4-scanline_timing.gb | ⏱ |
| 5-timing_bug.gb | ⏱ |
| 6-timing_no_bug.gb | ⏱ |
| 7-timing_effect.gb | ⏱ |
| 8-instr_effect.gb | ⏱ |

</details>

---

## cpp

### General — 0/3 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| latch-rtc-test.gb | ⏱ |
| ramg-mbc3-test.gb | ⏱ |
| rtc-invalid-banks-test.gb | ⏱ |

</details>

---

## daid

### General — 0/4 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| ppu_scanline_bgp.gb | ⏱ |
| rom_and_ram.gb | ⏱ |
| speed_switch_timing_div.gbc | ⊘ |
| speed_switch_timing_ly.gbc | ⊘ |
| speed_switch_timing_stat.gbc | ⊘ |
| stop_instr.gb | ⏱ |
| stop_instr_gbc_mode3.gb | ⏱ |

</details>

---

## hacktix

### General

*Visual comparison required*

---

## mealybug-tearoom-tests

### ppu

*Visual comparison required*

---

## mooneye

### acceptance — 4/41 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| add_sp_e_timing.gb | ⏱ |
| boot_div-S.gb | ⏱ |
| boot_div-dmg0.gb | ⏱ |
| boot_div-dmgABCmgb.gb | ⏱ |
| boot_div2-S.gb | ⏱ |
| boot_hwio-S.gb | ⏱ |
| boot_hwio-dmg0.gb | ⏱ |
| boot_hwio-dmgABCmgb.gb | ⏱ |
| boot_regs-dmg0.gb | ⏱ |
| boot_regs-dmgABC.gb | ✅ |
| boot_regs-mgb.gb | ⏱ |
| boot_regs-sgb.gb | ⏱ |
| boot_regs-sgb2.gb | ⏱ |
| call_cc_timing.gb | ⏱ |
| call_cc_timing2.gb | ⏱ |
| call_timing.gb | ⏱ |
| call_timing2.gb | ⏱ |
| di_timing-GS.gb | ⏱ |
| div_timing.gb | ✅ |
| ei_sequence.gb | ⏱ |
| ei_timing.gb | ⏱ |
| halt_ime0_ei.gb | ✅ |
| halt_ime0_nointr_timing.gb | ⏱ |
| halt_ime1_timing.gb | ✅ |
| halt_ime1_timing2-GS.gb | ⏱ |
| if_ie_registers.gb | ⏱ |
| intr_timing.gb | ⏱ |
| jp_cc_timing.gb | ⏱ |
| jp_timing.gb | ⏱ |
| ld_hl_sp_e_timing.gb | ⏱ |
| oam_dma_restart.gb | ⏱ |
| oam_dma_start.gb | ⏱ |
| oam_dma_timing.gb | ⏱ |
| pop_timing.gb | ⏱ |
| push_timing.gb | ⏱ |
| rapid_di_ei.gb | ⏱ |
| ret_cc_timing.gb | ⏱ |
| ret_timing.gb | ⏱ |
| reti_intr_timing.gb | ⏱ |
| reti_timing.gb | ⏱ |
| rst_timing.gb | ⏱ |

</details>

### acceptance/bits — 2/3 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| mem_oam.gb | ✅ |
| reg_f.gb | ✅ |
| unused_hwio-GS.gb | ⏱ |

</details>

### acceptance/instr — 1/1 ✅

All tests passing.

### acceptance/interrupts — 0/1 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| ie_push.gb | ⏱ |

</details>

### acceptance/oam_dma — 2/3 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| basic.gb | ✅ |
| reg_read.gb | ✅ |
| sources-GS.gb | ⏱ |

</details>

### acceptance/ppu — 1/12 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| hblank_ly_scx_timing-GS.gb | ⏱ |
| intr_1_2_timing-GS.gb | ⏱ |
| intr_2_0_timing.gb | ✅ |
| intr_2_mode0_timing.gb | ⏱ |
| intr_2_mode0_timing_sprites.gb | ⏱ |
| intr_2_mode3_timing.gb | ⏱ |
| intr_2_oam_ok_timing.gb | ⏱ |
| lcdon_timing-GS.gb | ⏱ |
| lcdon_write_timing-GS.gb | ⏱ |
| stat_irq_blocking.gb | ⏱ |
| stat_lyc_onoff.gb | ⏱ |
| vblank_stat_intr-GS.gb | ⏱ |

</details>

### acceptance/serial — 0/1 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| boot_sclk_align-dmgABCmgb.gb | ⏱ |

</details>

### acceptance/timer — 13/13 ✅

All tests passing.

### emulator-only/mbc1 — 13/13 ✅

All tests passing.

### emulator-only/mbc2 — 7/7 ✅

All tests passing.

### emulator-only/mbc5 — 8/8 ✅

All tests passing.

### manual-only — 0/1 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| sprite_priority.gb | ⏱ |

</details>

### misc — 0/6 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| boot_div-A.gb | ⏱ |
| boot_div-cgb0.gb | ⏱ |
| boot_div-cgbABCDE.gb | ⏱ |
| boot_hwio-C.gb | ⏱ |
| boot_regs-A.gb | ⏱ |
| boot_regs-cgb.gb | ⏱ |

</details>

### misc/bits — 0/1 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| unused_hwio-C.gb | ⏱ |

</details>

### misc/ppu — 0/1 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| vblank_stat_intr-C.gb | ⏱ |

</details>

---

## samesuite

### apu — 0/5 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| div_trigger_volume_10.gb | ⏱ |
| div_write_trigger.gb | 💥 |
| div_write_trigger_10.gb | 💥 |
| div_write_trigger_volume.gb | 💥 |
| div_write_trigger_volume_10.gb | 💥 |

</details>

### apu/channel_1 — 0/21 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| channel_1_align.gb | 💥 |
| channel_1_align_cpu.gb | 💥 |
| channel_1_delay.gb | 💥 |
| channel_1_duty.gb | 💥 |
| channel_1_duty_delay.gb | 💥 |
| channel_1_extra_length_clocking-cgb0B.gb | 💥 |
| channel_1_freq_change.gb | 💥 |
| channel_1_freq_change_timing-A.gb | 💥 |
| channel_1_freq_change_timing-cgb0BC.gb | 💥 |
| channel_1_freq_change_timing-cgbDE.gb | 💥 |
| channel_1_nrx2_glitch.gb | 💥 |
| channel_1_nrx2_speed_change.gb | 💥 |
| channel_1_restart.gb | 💥 |
| channel_1_restart_nrx2_glitch.gb | 💥 |
| channel_1_stop_div.gb | 💥 |
| channel_1_stop_restart.gb | 💥 |
| channel_1_sweep.gb | 💥 |
| channel_1_sweep_restart.gb | 💥 |
| channel_1_sweep_restart_2.gb | 💥 |
| channel_1_volume.gb | 💥 |
| channel_1_volume_div.gb | 💥 |

</details>

### apu/channel_2 — 0/15 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| channel_2_align.gb | 💥 |
| channel_2_align_cpu.gb | 💥 |
| channel_2_delay.gb | 💥 |
| channel_2_duty.gb | 💥 |
| channel_2_duty_delay.gb | 💥 |
| channel_2_extra_length_clocking-cgb0B.gb | 💥 |
| channel_2_freq_change.gb | 💥 |
| channel_2_nrx2_glitch.gb | 💥 |
| channel_2_nrx2_speed_change.gb | 💥 |
| channel_2_restart.gb | 💥 |
| channel_2_restart_nrx2_glitch.gb | 💥 |
| channel_2_stop_div.gb | 💥 |
| channel_2_stop_restart.gb | 💥 |
| channel_2_volume.gb | 💥 |
| channel_2_volume_div.gb | 💥 |

</details>

### apu/channel_3 — 1/15 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| channel_3_and_glitch.gb | 💥 |
| channel_3_delay.gb | 💥 |
| channel_3_extra_length_clocking-cgb0.gb | 💥 |
| channel_3_extra_length_clocking-cgbB.gb | 💥 |
| channel_3_first_sample.gb | 💥 |
| channel_3_freq_change_delay.gb | 💥 |
| channel_3_restart_delay.gb | 💥 |
| channel_3_restart_during_delay.gb | 💥 |
| channel_3_restart_stop_delay.gb | 💥 |
| channel_3_shift_delay.gb | 💥 |
| channel_3_shift_skip_delay.gb | 💥 |
| channel_3_stop_delay.gb | ✅ |
| channel_3_stop_div.gb | 💥 |
| channel_3_wave_ram_locked_write.gb | 💥 |
| channel_3_wave_ram_sync.gb | 💥 |

</details>

### apu/channel_4 — 0/13 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| channel_4_align.gb | 💥 |
| channel_4_delay.gb | 💥 |
| channel_4_equivalent_frequencies.gb | 💥 |
| channel_4_extra_length_clocking-cgb0B.gb | 💥 |
| channel_4_freq_change.gb | 💥 |
| channel_4_frequency_alignment.gb | 💥 |
| channel_4_lfsr.gb | 💥 |
| channel_4_lfsr15.gb | 💥 |
| channel_4_lfsr_15_7.gb | 💥 |
| channel_4_lfsr_7_15.gb | 💥 |
| channel_4_lfsr_restart.gb | 💥 |
| channel_4_lfsr_restart_fast.gb | 💥 |
| channel_4_volume_div.gb | 💥 |

</details>

### dma — 0/4 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| gbc_dma_cont.gb | 💥 |
| gdma_addr_mask.gb | 💥 |
| hdma_lcd_off.gb | 💥 |
| hdma_mode0.gb | 💥 |

</details>

### ppu — 0/1 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| blocking_bgpi_increase.gb | 💥 |

</details>

### sgb — 0/2 

<details>
<summary>Details</summary>

| Test | Result |
|---|---|
| command_mlt_req.gb | 💥 |
| command_mlt_req_1_incrementing.gb | 💥 |

</details>

