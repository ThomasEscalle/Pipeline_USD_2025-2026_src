#include "Debug.h"
#include "FileHelper.h"

int main(int argc, char* argv[]) {
    Debug::showStartupMessage();


    Debug::log("Demarage de l'application avec " + std::to_string(argc) + " arguments.");


    if (FileHelper::fileExists("C:/Users/Thomas/OneDrive/Bureau/Ce que je veux dans le moteur de jeux en.md")) {
        Debug::log("The file exists");
        
    }
    else {
        Debug::log("The file does not exists");
    }


    Debug::waitForEndInput();

    return 0;
}