#include "ppu.h"

PPU::PPU(Registers* registers, Interrupts* interrupts, MMU* mmu) {
    this->registers = registers;
    this->mmu = mmu;
    this->interrupts = interrupts;

    control = (Control*)&mmu->memory[0xff40];
    stat = (Stat*)&mmu->memory[0xff41];
    scrollY = &mmu->memory[0xff42];
    scrollX = &mmu->memory[0xff43];
    scanline = &mmu->memory[0xff44];
}

void PPU::step() {
    modeclock += mmu->clock.t_instr;

    if (!control->lcdEnable) {
        mode = 0;
        if (modeclock >= 70224)
            modeclock -= 70224;
        return;
    }

    switch (mode) {
        case 0:  // HBLANK
            if (modeclock >= 204) {
                modeclock -= 204;
                mode = 2;

                *scanline += 1;
                compare_ly_lyc();

                if (*scanline == 144) {
                    mode = 1;
                    can_render = true;
                    interrupts->set_interrupt_flag(INTERRUPT_VBLANK);
                    if (stat->vblank_interrupt)
                        interrupts->set_interrupt_flag(INTERRUPT_LCD);
                } else if (stat->oam_interrupt)
                    interrupts->set_interrupt_flag(INTERRUPT_LCD);

                mmu->memory[0xff41] = (mmu->memory[0xff41] & 0xFC) | (mode & 3);
            }
            break;
        case 1:  // VBLANK
            if (modeclock >= 456) {
                modeclock -= 456;
                *scanline += 1;
                compare_ly_lyc();
                if (*scanline == 153) {
                    *scanline = 0;
                    window_line = 0;
                    mode = 2;
                    mmu->memory[0xff41] = (mmu->memory[0xff41] & 0xFC) | (mode & 3);
                    if (stat->oam_interrupt)
                        interrupts->set_interrupt_flag(INTERRUPT_LCD);
                }
            }

            break;
        case 2:  // OAM
            if (modeclock >= 80) {
                modeclock -= 80;
                mode = 3;
                mmu->memory[0xff41] = (mmu->memory[0xff41] & 0xFC) | (mode & 3);
            }
            break;
        case 3:  // VRAM
            if (modeclock >= 172) {
                modeclock -= 172;
                mode = 0;
                render_scan_lines();
                mmu->memory[0xff41] = (mmu->memory[0xff41] & 0xFC) | (mode & 3);

                if (stat->hblank_interrupt)
                    interrupts->set_interrupt_flag(INTERRUPT_LCD);
            }
            break;
    }
}

void PPU::compare_ly_lyc() {
    // TODO: Modify so that we don't access the address directly and use read_byte
    uint8_t lyc = mmu->memory[0xFF45];
    stat->coincidence_flag = int(lyc == *scanline);

    if (lyc == *scanline && stat->coincidence_interrupt)
        this->interrupts->set_interrupt_flag(INTERRUPT_LCD);
}

void PPU::render_scan_lines() {
    bool row_pixels[160] = {0};
    this->render_scan_line_background(row_pixels);
    this->render_scan_line_window(row_pixels);
    this->render_scan_line_sprites(row_pixels);
}

void PPU::render_scan_line_background(bool* row_pixels) {
    if (!control->bgDisplay) {
        int pixelOffset = *this->scanline * 160;

        std::fill_n(&framebuffer[pixelOffset], 160, mmu->palette_BGP[0]);
        std::fill_n(row_pixels, 160, false);
        return;
    }

    uint16_t address = 0x9800;

    if (this->control->bgDisplaySelect)
        address += 0x400;

    address += ((*this->scrollY + *this->scanline) / 8 * 32) % (32 * 32);

    uint16_t start_row_address = address;
    uint16_t end_row_address = address + 32;
    address += (*this->scrollX >> 3);

    int x = *this->scrollX & 7;
    int y = (*this->scanline + *this->scrollY) & 7;
    int pixelOffset = *this->scanline * 160;

    int pixel = 0;
    for (int i = 0; i < 21; i++) {
        uint16_t tile_address = address + i;
        if (tile_address >= end_row_address)
            tile_address = (start_row_address + tile_address % end_row_address);

        int tile = this->mmu->memory[tile_address];
        if (!this->control->bgWindowDataSelect && tile < 128)
            tile += 256;

        for (; x < 8; x++) {
            if (pixel >= 160)
                break;

            int colour = mmu->tiles[tile].pixels[y][x];
            framebuffer[pixelOffset++] = mmu->palette_BGP[colour];
            if (colour > 0)
                row_pixels[pixel] = true;
            pixel++;
        }
        x = 0;
    }
}

void PPU::render_scan_line_window(bool* row_pixels) {
    if (!this->control->bgDisplay || !this->control->windowEnable)
        return;

    int wy = mmu->memory[0xFF4A];
    int wx = mmu->memory[0xFF4B] - 7;

    if (*this->scanline < wy || wx > 159)
        return;

    uint16_t address = this->control->windowDisplaySelect ? 0x9C00 : 0x9800;
    address += (window_line / 8) * 32;
    
    int y = window_line & 7;
    int pixelOffset = *this->scanline * 160;

    for (int i = 0; i < 20; i++) {
        int tile = this->mmu->memory[address + i];
        if (!this->control->bgWindowDataSelect && tile < 128)
            tile += 256;
        
        for (int x = 0; x < 8; x++) {
            int target_x = wx + (i * 8) + x;

            if (target_x >= 0 && target_x < 160) {
                int colour = mmu->tiles[tile].pixels[y][x];

                framebuffer[pixelOffset + target_x] = mmu->palette_BGP[colour];
                row_pixels[target_x] = (colour > 0);
            }
        }
    }
    window_line++;
}

void PPU::render_scan_line_sprites(bool* row_pixels) {
    if (!control->spriteDisplayEnable)
        return;

    int sprite_height = control->spriteSize ? 16 : 8;
    int sprites_found = 0;
    uint8_t sprite_indices[10]; 
    uint8_t pixel_sprite_x[160];
    std::fill_n(pixel_sprite_x, 160, 255);

    // Identify the first 10 valid sprites
    for (int i = 0; sprites_found < 10 && i < 40; i++) {
        auto& sprite = mmu->sprites[i];
        if (!sprite.ready)
            continue;

        if (sprite.y > *scanline || (sprite.y + sprite_height) <= *scanline)
            continue;
        
        sprite_indices[sprites_found++] = i;
    }

    // Render only those 10 sprites
    for (int i = 0; i < sprites_found; i++) {
        auto& sprite = mmu->sprites[sprite_indices[i]];
        
        // Flip vertically
        int pixel_y = *scanline - sprite.y;
        if (sprite.options.yFlip)
            pixel_y = (sprite_height - 1) - pixel_y;

        for (int x = 0; x < 8; x++) {
            int target_x = sprite.x + x;

            if (target_x < 0 || target_x >= 160)
                continue;
            
            if (sprite.x >= pixel_sprite_x[target_x])
                continue;

            // Flip horizontally
            uint8_t pixel_x = sprite.options.xFlip ? 7 - x : x;
            int tile_num = sprite.tile & (control->spriteSize ? 0xFE : 0xFF);
            
            int colour = 0;
            if (control->spriteSize && (pixel_y >= 8))
                colour = mmu->tiles[tile_num + 1].pixels[pixel_y - 8][pixel_x];
            else
                colour = mmu->tiles[tile_num].pixels[pixel_y][pixel_x];

            // Black is transparent
            if (!colour)
                continue;

            if (!row_pixels[target_x] || !sprite.options.renderPriority) {
                framebuffer[*scanline * 160 + target_x] = sprite.colourPalette[colour];
                pixel_sprite_x[target_x] = sprite.x;
            }
        }
    }
}