#include <iostream>
#include <string>


class Debug {
public:
    static void log(const std::string& message);

    static void err(const std::string& message);

    static void showStartupMessage();

    static void waitForEndInput();
};

