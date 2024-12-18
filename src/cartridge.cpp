#include "cartridge.h"

Cartridge::Cartridge(std::string rom, std::string save_file) {
    load_game_rom(rom);
    load_save_state(save_file);
}

void Cartridge::load_game_rom(std::string location) {
    std::ifstream GAME_ROM(location, std::ios::binary);
    GAME_ROM.seekg(0, std::ios::end);
    long size = GAME_ROM.tellg();
    if (size % (16 * 1024) != 0) {
        std::cout << "Size must be a multiple of 16 KB" << std::endl;
        return;
    }

    memory = new uint8_t[size];

    GAME_ROM.seekg(std::ios::beg);
    GAME_ROM.read((char *)memory, size);

    rom_banks_count = size / 0x4000;
    ram_banks_count = get_ram_banks_count(memory[0x149]);

    ram = new uint8_t[ram_banks_count * 0x2000];

    rom_title = std::string(memory + 0x134, memory + 0x143);
    cgb_game = memory[0x143] == 0x80 || memory[0x143] == 0xC0;
    mbc_type = memory[0x147];

    detect_mbc_type(memory[0x147]);

    this->printInfo();
}

void Cartridge::detect_mbc_type(uint8_t type) {
    switch (type) {
        case 0x00:
        case 0x08:
        case 0x09:
            mbc = new MBC0(memory);
            break;
        case 0x01:
        case 0x02:
        case 0x03:
            mbc = new MBC1(memory, ram, rom_banks_count, ram_banks_count);
            break;
        case 0x05:
        case 0x06:
            mbc = new MBC2(memory, ram, rom_banks_count, ram_banks_count);
            break;
        case 0x0F:
        case 0x10:
        case 0x11:
        case 0x12:
        case 0x13:
            mbc = new MBC3(memory, ram, rom_banks_count, ram_banks_count);
            break;
        case 0x19:
        case 0x1A:
        case 0x1B:
        case 0x1C:
        case 0x1D:
        case 0x1E:
            mbc = new MBC5(memory, ram, rom_banks_count, ram_banks_count);
            break;
        default:
            std::cout << "Unsupported MBC type: " << type << std::endl;
            exit(1);
    }
}

int Cartridge::get_ram_banks_count(uint8_t type) {
    switch (type) {
        case 0x00:
            return 0;
            break;
        case 0x01:
            return 0;
            break;
        case 0x02:
            return 1;
            break;
        case 0x03:
            return 4;
            break;
        case 0x04:
            return 16;
            break;
        case 0x05:
            return 8;
            break;
        default:
            std::cout << "Incorrect RAM type: " << type << std::endl;
            exit(1);
    }
}

void Cartridge::load_save_state(std::string save_file) {
    if (save_file.empty())
        return;

    std::ifstream SAVE(save_file, std::ios::binary);
    SAVE.seekg(0, std::ios::end);

    long size = SAVE.tellg();
    if (size != (0x7f * 0x2000 + sizeof(rom_title))) {
        std::cout << "Save file possibly corrupted. Save not loaded." << std::endl;
        return;
    }

    char save_title[16];
    SAVE.seekg(0, std::ios::beg);
    SAVE.read((char *)save_title, sizeof(save_title));
    std::cout << "Save file " << save_title << std::endl;
    if (rom_title != save_title) {
        std::cout << "This save file is not for this rom. Save not loaded." << std::endl;
        return;
    }
    SAVE.seekg(sizeof(save_title));
    SAVE.read((char *)ram, 0x7f * 0x2000);

    std::cout << "Save file loaded successfully" << std::endl;
}

void Cartridge::write_save_state() {
    std::filesystem::create_directory("saves");

    auto t = std::time(nullptr);
    auto tm = *std::localtime(&t);
    std::ostringstream oss;
    oss << "saves/" << rom_title << "_" << std::put_time(&tm, "%d-%m-%Y %H-%M-%S") << ".save";
    std::string filename = oss.str();

    std::ofstream out(filename, std::ios_base::binary);

    size_t title_length = rom_title.size();
    out.write(reinterpret_cast<const char *>(&title_length), sizeof(title_length));
    out.write(rom_title.c_str(), title_length);

    // Write the RAM data
    out.write(reinterpret_cast<const char *>(ram), sizeof(uint8_t) * (0x7f * 0x2000));

    std::cout << "Saved state to: " << filename << std::endl;
}

void Cartridge::printInfo() {
    std::cout << "Rom Title: " << rom_title << std::endl;
    std::cout << "CGB Game: " << (cgb_game ? "Yes" : "No") << std::endl;
    std::cout << "MBC: " << +mbc_type << std::endl;
    std::cout << "ROM Banks: " << rom_banks_count << std::endl;
    std::cout << "RAM Banks: " << ram_banks_count << std::endl;
}