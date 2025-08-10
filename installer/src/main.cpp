#include "Debug.h"
#include "FileHelper.h"


void createNewProject() {
    Debug::clearScreen();
    Debug::title("Creation d'un nouveau projet");
    Debug::newLine();
    std::string projectName = Debug::askForInput("Entrez le nom de votre projet : ");


    Debug::clearScreen();
    Debug::title("Creation d'un nouveau projet");
    Debug::newLine();
    Debug::showVariable("Nom du projet:", projectName);
    Debug::newLine();
    std::string projectPath = Debug::askForInput("Entrez le chemin du projet : ");


    Debug::clearScreen();
    Debug::title("Creation d'un nouveau projet");
    Debug::newLine();
    Debug::showVariable("Nom du projet:", projectName);
    Debug::showVariable("Chemin du projet:", projectPath);
    Debug::newLine();




    Debug::log("Creation du projet : " + projectName);
    // Ajoutez ici la logique pour créer un nouveau projet
}

void installPipeline() {
    Debug::log("Installation en cours ..");



}

int main(int argc, char* argv[]) {
    Debug::showStartupMessage();

    int choice = Debug::askForChoice("Que souhaitez vous faire ? ", { "Installer le pipeline sur cet ordinateur" , "Creer un nouveau projet" });
    if (choice == 0) {
        installPipeline();
    } else if (choice == 1) {
        createNewProject();
    }

    /// Success
    Debug::log("Installation du Pipeline sur cette machine reussie.");




    Debug::waitForEndInput();

    return 0;
}