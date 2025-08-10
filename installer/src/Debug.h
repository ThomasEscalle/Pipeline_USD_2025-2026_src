#include <iostream>
#include <string>
#include <vector>


class Debug {
public:
    static void log(const std::string& message);

    static void err(const std::string& message);

    static void showStartupMessage();

    static void waitForEndInput();

    static bool askForConfirmation(const std::string& question);

    static std::string askForInput(const std::string& prompt);

    static int askForChoice(const std::string& prompt, const std::vector<std::string>& choices);

    static void clearScreen();

    static void title(const std::string& title);

    static void newLine();

    static void showVariable(const std::string& name, const std::string& value);
};

