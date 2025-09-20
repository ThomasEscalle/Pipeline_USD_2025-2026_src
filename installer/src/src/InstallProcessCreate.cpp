#include "InstallProcessCreate.h"
#include <QStandardPaths>

#include "FileHelper.h"

InstallProcessCreate::InstallProcessCreate(QObject *parent)
{
}

InstallProcessCreate::~InstallProcessCreate()
{
}



bool InstallProcessCreate::install()
{
    log("Project name: " + m_projectName);
    log("Project path: " + m_projectPath);
    log(" ");
    processEvents();

    /// Verify the installation parameters
    if(!verify())
    {
        logError("Installation parameters are not valid. Aborting the creation of the project.");
        logError("Check the logs for more information.");
        emit this->installationFinished();
        return false;
    }
    processEvents();

    log("Creating project '" + m_projectName + "' in path '" + m_projectPath + "'...");

    processEvents();

    QString fullProjectPath = FileHelper::JoinPath(m_projectPath, m_projectName);

    /// Create the main project folder
    if(!FileHelper::CreateDir(fullProjectPath))
    {
        logError("Failed to create the project folder in path '" + fullProjectPath + "'.");
        emit this->installationFinished();
        return false;
    }


    processEvents();

    //// Create the project structure
    if(!createProjectStructure(fullProjectPath))
    {
        logError("Failed to create the project structure in path '" + fullProjectPath + "'.");
        emit this->installationFinished();
        return false;
    }

    processEvents();

    //// Fill the pipeline folder with the default files and folders
    QString pipelinePath = FileHelper::JoinPath(fullProjectPath, "00_Pipeline");
    if(!fillPipelineFolder(pipelinePath))
    {
        logError("Failed to fill the pipeline folder in path '" + pipelinePath + "'.");
        emit this->installationFinished();
        return false;
    }

    processEvents();








    /// DONE
    logSuccess("Project '" + m_projectName + "' created successfully in path '" + m_projectPath + "'.");
    emit this->installationFinished();
    return true;
}


bool InstallProcessCreate::verify()
{
    if(m_projectName.isEmpty())
    {
        logError("Project name is empty.");
        return false;
    }

    if(m_projectPath.isEmpty())
    {
        logError("Project path is empty.");
        return false;
    }

    // Check if the path exists
    if(!FileHelper::DirExists(m_projectPath))
    {
        logError("Project path '" + m_projectPath + "' does not exist.");
        return false;
    }

    /// Check if there is no a folder with the same name as the project in the given path
    QString fullProjectPath = FileHelper::JoinPath(m_projectPath, m_projectName);
    if(FileHelper::DirExists(fullProjectPath))
    {
        logError("A folder with the name '" + m_projectName + "' already exists in the path '" + m_projectPath + "'.");
        return false;
    }


    /// Check if there is a resources folder in the executable path
    QString pipelineTemplatePath = FileHelper::JoinPath( FileHelper::GetResourcesPath() , "00_Pipeline");
    if(!FileHelper::DirExists(pipelineTemplatePath))
    {
        logError("Pipeline template folder does not exist in the resources path.");
        logError("Expected path: '" + pipelineTemplatePath + "'.");
        return false;
    }

    return true;
}

bool InstallProcessCreate::createProjectStructure(const QString &fullProjectPath)
{
    /// Root folders

    // Create a 00_Pipeline folder
    if(!createFolder(fullProjectPath, "00_Pipeline")) return false;
    // Create a 01_Management folder
    if(!createFolder(fullProjectPath, "01_Management")) return false;
    // Create a 02_PreProd folder
    if(!createFolder(fullProjectPath, "02_PreProd")) return false;
    // Create a 03_Production folder
    if(!createFolder(fullProjectPath, "03_Production")) return false;
    // Create a 04_Editing folder
    if(!createFolder(fullProjectPath, "04_Editing")) return false;
    // Create a 05_Archives folder
    if(!createFolder(fullProjectPath, "05_Archives")) return false;
    // Create a 06_Resources folder
    if(!createFolder(fullProjectPath, "06_Resources")) return false;
    // Create a 07_Linetest folder
    if(!createFolder(fullProjectPath, "07_Linetest")) return false;
    // Create a 08_Dev folder
    if(!createFolder(fullProjectPath, "08_Dev")) return false;
    // Create a 09_Communication folder
    if(!createFolder(fullProjectPath, "09_Communication")) return false;


    //////// PIPELINE FOLDERS  ////////
    /// Todo latter


    //////// MANAGEMENT FOLDERS  ////////
    QString mgmtPath = FileHelper::JoinPath(fullProjectPath, "01_Management");
    // Create a readme file in the 01_Management folder
    if(!createReadmeFile(mgmtPath, "Ce dossier est dédié à la gestion du projet. Tu peux y stocker les liens vers les docs de prod, les plannings, les contrats, etc.")) return false;


    //////// PRE-PROD FOLDERS  ////////
    QString preprodPath = FileHelper::JoinPath(fullProjectPath, "02_PreProd");
    // Create a 01_Scenario folder
    if(!createFolder(preprodPath, "01_Scenario")) return false;
    // Create a 02_Concept folder
    if(!createFolder(preprodPath, "02_Concept")) return false;
    // Create a 02_Concept/01_Mood folder
    if(!createFolder(preprodPath, "02_Concept/01_Mood")) return false;
    if(!createReadmeFile(FileHelper::JoinPath(preprodPath, "02_Concept/01_Mood"), "Tu peux mettre ici les moodboards, les palettes de couleurs, les inspirations, etc.")) return false;
    // Create a 02_Concept/02_Char folder
    if(!createFolder(preprodPath, "02_Concept/02_Char")) return false;
    if(!createReadmeFile(FileHelper::JoinPath(preprodPath, "02_Concept/02_Char"), "Tu peux créer ici un dossier par personnage, avec des sous-dossiers pour les edits et les références.")) return false;
    if(!createFolder(preprodPath, "02_Concept/02_Char/nom_du_char")) return false;
    if(!createFolder(preprodPath, "02_Concept/02_Char/nom_du_char/edits")) return false;
    if(!createFolder(preprodPath, "02_Concept/02_Char/nom_du_char/references")) return false;
    // Create a 02_Concept/03_Env folder
    if(!createFolder(preprodPath, "02_Concept/03_Enviro")) return false;
    if(!createReadmeFile(FileHelper::JoinPath(preprodPath, "02_Concept/03_Enviro"), "Tu peux créer ici un dossier par environnement, avec des sous-dossiers pour les edits et les références.")) return false;
    if(!createFolder(preprodPath, "02_Concept/03_Enviro/nom_de_l_env")) return false;
    if(!createFolder(preprodPath, "02_Concept/03_Enviro/nom_de_l_env/edits")) return false;
    if(!createFolder(preprodPath, "02_Concept/03_Enviro/nom_de_l_env/references")) return false;
    // Create a 02_Concept/04_Props folder
    if(!createFolder(preprodPath, "02_Concept/04_Props")) return false;
    if(!createReadmeFile(FileHelper::JoinPath(preprodPath, "02_Concept/04_Props"), "Tu peux créer ici un dossier par props, avec des sous-dossiers pour les edits et les références.")) return false;
    if(!createFolder(preprodPath, "02_Concept/04_Props/nom_du_props")) return false;
    if(!createFolder(preprodPath, "02_Concept/04_Props/nom_du_props/edits")) return false;
    if(!createFolder(preprodPath, "02_Concept/04_Props/nom_du_props/references")) return false;
    // Create a 02_Concept/05_Keyshot folder
    if(!createFolder(preprodPath, "02_Concept/05_Keyshot")) return false;
    if(!createReadmeFile(FileHelper::JoinPath(preprodPath, "02_Concept/05_Keyshot"), "Tu peux créer ici un dossier par keyshot, avec des sous-dossiers pour les edits et les références.")) return false;
    if(!createFolder(preprodPath, "02_Concept/05_Keyshot/nom_du_keyshot")) return false;
    if(!createFolder(preprodPath, "02_Concept/05_Keyshot/nom_du_keyshot/edits")) return false;
    if(!createFolder(preprodPath, "02_Concept/05_Keyshot/nom_du_keyshot/references")) return false;
    // Create a 03_Storyboard folder
    if(!createFolder(preprodPath, "03_Storyboard")) return false;
    // Create a 04_Color_Script folder
    if(!createFolder(preprodPath, "04_Color_Script")) return false;
    // Create a 05_Cinematography folder
    if(!createFolder(preprodPath, "05_Cinematography")) return false;
    if(!createReadmeFile(FileHelper::JoinPath(preprodPath, "05_Cinematography"), "Ce dossier est dédié a la collecte de références pour la cinématographie.")) return false;


    //////// PRODUCTION FOLDERS  ////////
    QString prodPath = FileHelper::JoinPath(fullProjectPath, "03_Production");
    // Create a 01_Assets folder
    if(!createFolder(prodPath, "01_Assets")) return false;
    // Create a 01_Assets/Chars folder
    if(!createFolder(prodPath, "01_Assets/Chars")) return false;
    // Create a 01_Assets/Items folder
    if(!createFolder(prodPath, "01_Assets/Items")) return false;
    // Create a 01_Assets/Modules folder
    if(!createFolder(prodPath, "01_Assets/Modules")) return false;
    // Create a 01_Assets/Props folder
    if(!createFolder(prodPath, "01_Assets/Props")) return false;
    // Create a 02_Shots folder
    if(!createFolder(prodPath, "02_Shots")) return false;


    //////// EDITING FOLDERS  ////////
    QString editPath = FileHelper::JoinPath(fullProjectPath, "04_Editing");
    // Nothing for now

    ////////  ARCHIVES FOLDERS  ////////
    QString archPath = FileHelper::JoinPath(fullProjectPath, "05_Archives");
    // Nothing for now

    //////// RESOURCES FOLDERS  ////////
    QString resPath = FileHelper::JoinPath(fullProjectPath, "06_Resources");
    // Create a Artistes folder
    if(!createFolder(resPath, "Artistes")) return false;
    if(!createFolder(resPath, "Artistes/nom_de_l_artiste")) return false;
    if(!createReadmeFile(FileHelper::JoinPath(resPath, "Artistes/nom_de_l_artiste"), "Ici, chaque artiste peut faire ce qu'il veut. Attention à ne pas stocker des fichiers utilisés en prod qui seront référencés par le pipeline principal (geo, textures...).")) return false;
    // Create a Professeurs folder
    if(!createFolder(resPath, "Professeurs/nom_du_professeur")) return false;
    if(!createReadmeFile(FileHelper::JoinPath(resPath, "Professeurs/nom_du_professeur"), "Ici, on stocke eventuellement des fichiers de ressources données par les professeur.")) return false;
    // Create a Externals folder
    if(!createFolder(resPath, "Externals")) return false;

    //////// LINETEST FOLDERS  ////////
    QString linePath = FileHelper::JoinPath(fullProjectPath, "07_Linetest");
    // Create a 01_Jury folder
    if(!createFolder(linePath, "01_Jury")) return false;
    if(!createFolder(linePath, "01_Jury/jury_001")) return false;
    // Create a 02_ReviewProd folder
    if(!createFolder(linePath, "02_ReviewProd")) return false;
    if(!createFolder(linePath, "02_ReviewProd/reviewprod_001")) return false;
    // Create a 03_ReviewDepartements folder
    if(!createFolder(linePath, "03_ReviewDepartements")) return false;

    //////// DEV FOLDERS  ////////
    QString devPath = FileHelper::JoinPath(fullProjectPath, "08_Dev");
    // Create a Dev_pipeline_tools folder
    if(!createFolder(devPath, "Dev_pipeline_tools")) return false;
    // Create a Dev_maya_tools folder
    if(!createFolder(devPath, "Dev_maya_tools")) return false;
    // Create a Dev_nuke_tools folder
    if(!createFolder(devPath, "Dev_nuke_tools")) return false;
    // Create a Dev_houdini_tools folder
    if(!createFolder(devPath, "Dev_houdini_tools")) return false;
    // Create a Dev_substance_tools folder
    if(!createFolder(devPath, "Dev_substance_tools")) return false;
    // Create a Dev_zbrush_tools folder
    if(!createFolder(devPath, "Dev_zbrush_tools")) return false;


    //////// COMMUNICATION FOLDERS  ////////
    QString commPath = FileHelper::JoinPath(fullProjectPath, "09_Communication");
    // 01_Prints folder
    if(!createFolder(commPath, "01_Prints")) return false;
    if(!createFolder(commPath, "01_Prints/Affiches")) return false;
    if(!createFolder(commPath, "01_Prints/Flyers")) return false;
    if(!createFolder(commPath, "01_Prints/Cartes_de_visite")) return false;
    if(!createFolder(commPath, "01_Prints/Autres")) return false;
    // 02_Reseaux_sociaux folder
    if(!createFolder(commPath, "02_Reseaux_sociaux")) return false;
    if(!createFolder(commPath, "02_Reseaux_sociaux/Instagram")) return false;
    if(!createFolder(commPath, "02_Reseaux_sociaux/Facebook")) return false;
    if(!createFolder(commPath, "02_Reseaux_sociaux/Twitter")) return false;
    if(!createFolder(commPath, "02_Reseaux_sociaux/Youtube")) return false;
    if(!createFolder(commPath, "02_Reseaux_sociaux/Linkedin")) return false;
    if(!createFolder(commPath, "02_Reseaux_sociaux/TikTok")) return false;
    if(!createFolder(commPath, "02_Reseaux_sociaux/TheRookies")) return false;
    if(!createFolder(commPath, "02_Reseaux_sociaux/ArtStation")) return false;

    // 03_Festivals folder
    if(!createFolder(commPath, "03_Festivals")) return false;
    // 04_Bandes_annonces folder
    if(!createFolder(commPath, "04_Bandes_annonces")) return false;

    return true;
}

bool InstallProcessCreate::fillPipelineFolder(const QString &pipelinePath)
{

    QString pipelineTemplatePath = FileHelper::JoinPath( FileHelper::GetResourcesPath() , "00_Pipeline");

    // Create a readme file in the 00_Pipeline folder
    if(!createReadmeFile(pipelinePath, "Ce dossier est le coeur du fonctionnement du pipeline. Il ne faut pas le modifier manuellement, sauf si tu sais ce que tu fais.")) return false;

    /// Create the default sub-folders
    // Assetinfo
    if(!createFolder(pipelinePath, "Assetinfo")) return false;
    // Commands
    if(!createFolder(pipelinePath, "Commands")) return false;
    // Configs
    if(!createFolder(pipelinePath, "Configs")) return false;
    // CustomModules
    if(!createFolder(pipelinePath, "CustomModules")) return false;
    // Fallbacks
    if(!createFolder(pipelinePath, "Fallbacks")) return false;
    // HDRIs
    if(!createFolder(pipelinePath, "HDRIs")) return false;
    // Hooks
    if(!createFolder(pipelinePath, "Hooks")) return false;
    // Icons
    if(!createFolder(pipelinePath, "Icons")) return false;
    // Plugins
    if(!createFolder(pipelinePath, "Plugins")) return false;
    // PresetScenes
    if(!createFolder(pipelinePath, "PresetScenes")) return false;
    // Shotinfo
    if(!createFolder(pipelinePath, "Shotinfo")) return false;
    // Templates
    if(!createFolder(pipelinePath, "Templates")) return false;


    /// Create the files in the pipeline folder

    /// Assetinfo folder
    // Create an empty JSON object file named "assetInfo.json"
    if(!createEmptyJsonObjectFile(FileHelper::JoinPath(pipelinePath, "Assetinfo/assetInfo.json"))) return false;

    /// Commands folder
    // Do nothing for now

    /// Configs folder
    // Create an empty JSON object file named "omits.json"
    if(!createEmptyJsonObjectFile(FileHelper::JoinPath(pipelinePath, "Configs/omits.json"))) return false;
    if(!copyFile(
                FileHelper::JoinPath(pipelineTemplatePath, "Configs/codePresets.json"),
                FileHelper::JoinPath(pipelinePath, "Configs/codePresets.json")
                )) return false;

    /// CustomModules folder
    // Create a readme file in the CustomModules folder
    if(!createReadmeFile(FileHelper::JoinPath(pipelinePath, "CustomModules"), "The CustomModules/Python folder gets appended to the PATH environment variable by Prism. You can place 3rd party python modules in there, which you want to use in your hooks/Prism-plugins/custom scripts.")) return false;
    if(!createFolder(FileHelper::JoinPath(pipelinePath, "CustomModules"), "Python")) return false;

    /// Fallbacks
    if(!copyAllContainedFilesToFolder( FileHelper::JoinPath(pipelineTemplatePath, "Fallbacks") , FileHelper::JoinPath(pipelinePath, "Fallbacks") )) return false;

    /// HDRIs folder
    // Create an empty JSON object file named "calibration.json"
    if(!createEmptyJsonObjectFile(FileHelper::JoinPath(pipelinePath, "HDRIs/calibration.json"))) return false;

    /// Hooks folder
    if(!copyAllContainedFilesToFolder( FileHelper::JoinPath(pipelineTemplatePath, "Hooks") , FileHelper::JoinPath(pipelinePath, "Hooks") )) return false;

    // Icons
    if(!copyAllContainedFilesToFolder( FileHelper::JoinPath(pipelineTemplatePath, "Icons") , FileHelper::JoinPath(pipelinePath, "Icons") )) return false;

    /// Plugins
    if(!copyAllContainedFilesToFolder( FileHelper::JoinPath(pipelineTemplatePath, "Plugins") , FileHelper::JoinPath(pipelinePath, "Plugins") )) return false;

    /// PresetScenes
    if(!copyAllContainedFilesToFolder( FileHelper::JoinPath(pipelineTemplatePath, "PresetScenes") , FileHelper::JoinPath(pipelinePath, "PresetScenes") )) return false;

    /// Shotinfo folder
    // Create an empty JSON object file named "shotInfo.json"
    if(!createEmptyJsonObjectFile(FileHelper::JoinPath(pipelinePath, "Shotinfo/shotInfo.json"))) return false;
    
    /// Templates folder
    if(!copyAllContainedFilesToFolder( FileHelper::JoinPath(pipelineTemplatePath, "Templates") , FileHelper::JoinPath(pipelinePath, "Templates") )) return false;


    //// OTHER FILES

    // bookmarks.json
    if(!copyFile(
                FileHelper::JoinPath(pipelineTemplatePath, "bookmarks.json"),
                FileHelper::JoinPath(pipelinePath, "bookmarks.json")
                )) return false;

    // links.json
    if(!copyFile(
                FileHelper::JoinPath(pipelineTemplatePath, "links.json"),
                FileHelper::JoinPath(pipelinePath, "links.json")
                )) return false;

    // project.jpg
    if(!copyFile(
                FileHelper::JoinPath(pipelineTemplatePath, "project.jpg"),
                FileHelper::JoinPath(pipelinePath, "project.jpg")
                )) return false;
    



    // pipeline.json
    if(!copyFile(
                FileHelper::JoinPath(pipelineTemplatePath, "pipeline.json"),
                FileHelper::JoinPath(pipelinePath, "pipeline.json")
                )) return false;
    // Replace the placeholder $$PROJECT_NAME$$ with the actual project name in the pipeline.json file
    if(!replaceInFile(
                FileHelper::JoinPath(pipelinePath, "pipeline.json"),
                "$$PROJECT_NAME$$",
                m_projectName
                )) return false;
    


    return true;
}





QString InstallProcessCreate::projectName() const
{
    return m_projectName;
}

void InstallProcessCreate::setProjectName(const QString &newProjectName)
{
    m_projectName = newProjectName;
}

QString InstallProcessCreate::projectPath() const
{
    return m_projectPath;
}

void InstallProcessCreate::setProjectPath(const QString &newProjectPath)
{
    m_projectPath = newProjectPath;
}

bool InstallProcessCreate::createFolder(const QString &path, const QString &folderName)
{
    QString fullPath = FileHelper::JoinPath(path, folderName);
    if(!FileHelper::CreateDir(fullPath))
    {
        logError("Failed to create folder '" + folderName + "' in path '" + path + "'.");
        return false;
    }
    log("Created folder: " + fullPath);
    processEvents();
    return true;
}

bool InstallProcessCreate::createReadmeFile(const QString &path, const QString &content)
{
    QString filePath = FileHelper::JoinPath(path, "readme.txt");
    if(!FileHelper::WriteFile(filePath, content))
    {
        logError("Failed to create readme file in path '" + path + "'.");
        return false;
    }
    log("Created readme file: " + filePath);
    processEvents();
    return true;
}

bool InstallProcessCreate::createEmptyJsonObjectFile(const QString &path)
{
    QString filePath = path;
    if(!FileHelper::WriteFile(filePath, "{}"))
    {
        logError("Failed to create empty JSON object file in path '" + path + "'.");
        return false;
    }
    log("Created empty JSON object file: " + filePath);
    processEvents();
    return true;
}

bool InstallProcessCreate::createEmptyJsonArrayFile(const QString &path)
{
    QString filePath = path;
    if(!FileHelper::WriteFile(filePath, "[]"))
    {
        logError("Failed to create empty JSON array file in path '" + path + "'.");
        return false;
    }
    log("Created empty JSON array file: " + filePath);
    processEvents();
    return true;
}

bool InstallProcessCreate::copyFile(const QString &sourcePath, const QString &destPath)
{
    if(!FileHelper::CopyFile(sourcePath, destPath))
    {
        logError("Failed to copy file from '" + sourcePath + "' to '" + destPath + "'.");
        return false;
    }
    log("Copied file from '" + sourcePath + "' to '" + destPath + "'.");
    processEvents();
    return true;

}

bool InstallProcessCreate::copyAllContainedFilesToFolder(const QString &sourceFolder, const QString &destFolder)
{
    QStringList files = FileHelper::GetAllFilesInFolder(sourceFolder);
    for(const QString& filePath : files)
    {
        QString destFilePath = FileHelper::JoinPath(destFolder, FileHelper::GetFileNameFromPath(filePath));
        if(!copyFile(filePath, destFilePath))
        {
            logError("Failed to copy file '" + filePath + "' to folder '" + destFolder + "'.");
            return false;
        }
        log("Copied file '" + filePath + "' to folder '" + destFolder + "'.");
        processEvents();
    }
    return true;

}


bool InstallProcessCreate::replaceInFile(const QString &filePath, const QString &placeholder, const QString &value)
{
    QString content;
    if(!FileHelper::ReadFile(filePath, content))
    {
        logError("Failed to read file '" + filePath + "' for replacement.");
        return false;
    }

    content.replace(placeholder, value);

    if(!FileHelper::WriteFile(filePath, content))
    {
        logError("Failed to write file '" + filePath + "' after replacement.");
        return false;
    }

    log("Replaced '" + placeholder + "' with '" + value + "' in file '" + filePath + "'.");
    processEvents();
    return true;
}