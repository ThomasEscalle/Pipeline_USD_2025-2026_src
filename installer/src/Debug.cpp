
#include "Debug.h"

// ANSI color codes
constexpr const char *RESET = "\033[0m";
constexpr const char *RED = "\033[31m";
constexpr const char *YELLOW = "\033[33m";
constexpr const char *CYAN = "\033[36m";
constexpr const char *WHITE = "\033[37m";
constexpr const char *BLUE = "\033[34m";


void Debug::log(const std::string& message) {
    std::cout << BLUE << "[DEBUG] " << RESET << message << std::endl;
}

void Debug::err(const std::string& message) {
    std::cerr << RED << "[ERROR] " << RESET << message << std::endl;
}

void Debug::showStartupMessage() {
    std::cout << CYAN;
    std::cout << "  ____            _                   _____           _        _ _           " << std::endl;
    std::cout << " |  _ \\          | |                 |_   _|         | |      | | |          " << std::endl;
    std::cout << " | |_) | __ _  __| | __ _  ___ _ __    | |  _ __  ___| |_ __ _| | | ___ _ __ " << std::endl;
    std::cout << " |  _ < / _` |/ _` |/ _` |/ _ \\ '__|   | | | '_ \\/ __| __/ _` | | |/ _ \\ '__|" << std::endl;
    std::cout << " | |_) | (_| | (_| | (_| |  __/ |     _| |_| | | \\__ \\ || (_| | | |  __/ |   " << std::endl;
    std::cout << " |____/ \\__,_|\\__,_|\\__, |\\___|_|    |_____|_| |_|___/\\__\\__,_|_|_|\\___|_|   " << std::endl;
    std::cout << "                     __/ |                                                   " << std::endl;
    std::cout << "                    |___/                                                    " << std::endl;
    std::cout << RESET << std::endl;
    std::cout << "Version 1.0.0" << std::endl;
    std::cout << "ESMA 2025 - 2026" << std::endl;
    std::cout << std::endl;
}

void Debug::waitForEndInput() {
    std::cout << std::endl;
    std::cout << "Appuyez sur nimporte quelle touche pour quitter" << std::endl;
    std::cin.get();
}
