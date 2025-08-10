
#include "Debug.h"

// ANSI color codes
constexpr const char *RESET = "\033[0m";
constexpr const char *RED = "\033[31m";
constexpr const char *YELLOW = "\033[33m";
constexpr const char *CYAN = "\033[36m";
constexpr const char *WHITE = "\033[37m";
constexpr const char *BLUE = "\033[34m";


void Debug::log(const std::string& message) {
    std::cout << CYAN << "[DEBUG] " << RESET << message << std::endl;
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
}

void Debug::waitForEndInput() {
    std::cout << std::endl;
    std::cout << "Appuyez sur nimporte quelle touche pour quitter" << std::endl;
    std::cin.get();
}


bool Debug::askForConfirmation(const std::string& question) {
    /// Check if the user's input is valid
    bool answerCorrect = false;

    /// Loop while the user did not provide a valid answer
    while(!answerCorrect) {
        std::cout << question << " (o/n) : ";
        char response;
        std::cin >> response;
        if(response == 'o' || response == 'O') {
            return true;
        } else if (response == 'n' || response == 'N') {
            return false;
        }
    }
    return answerCorrect;
}

std::string Debug::askForInput(const std::string& prompt) {
    std::cout << prompt;
    std::string input;
    std::getline(std::cin, input);
    std::cout << std::endl;
    return input;
}



int Debug::askForChoice(const std::string& prompt, const std::vector<std::string>& choices) {
    bool validChoice = false;
    int choice = 0;

    while (!validChoice) {
        std::cout << std::endl;
        std::cout << CYAN << prompt << RESET << std::endl;
        for (size_t i = 0; i < choices.size(); ++i) {
            std::cout << YELLOW << "  [ " << i + 1 << " ] " << RESET << " " << choices[i] << std::endl;
        }
        std::cout << "Entrez votre choix : ";
        std::cin >> choice;

        if (choice >= 1 && choice <= static_cast<int>(choices.size())) {
            validChoice = true;
        } else {
            std::cout << "Choix invalide. Veuillez reessayer." << std::endl;
        }
    }

    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');  // Clear the input buffer
    std::cout << std::endl;
    return choice - 1;

}


void Debug::clearScreen() {
    std::cout << "\033[2J\033[1;1H";  // ANSI escape code to clear the screen
}

void Debug::title(const std::string& title) {
    std::cout << CYAN << title << RESET << std::endl;
}

void Debug::newLine()
{
    std::cout << std::endl;
}

void Debug::showVariable(const std::string& name, const std::string& value)
{
    std::cout << name << CYAN << " " << value << RESET << std::endl;
}
