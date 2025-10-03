#include "InstallProcessTools.h"
#include <QStandardPaths>
#include "SoftwareHelpers.h"
#include "FileHelper.h"
#include "QDir"
#include "QFileInfo"
#include <QElapsedTimer>

InstallProcessTools::InstallProcessTools(QObject *parent)
{
}

InstallProcessTools::~InstallProcessTools()
{
}

bool InstallProcessTools::install()
{
    // Démarrer le timer pour mesurer le temps d'installation
    QElapsedTimer timer;
    timer.start();
    
    // Réinitialiser les listes de résultats
    m_successfulComponents.clear();
    m_failedComponents.clear();
    
    log("Starting installation process...");
    processEvents();

    /// Verify the installation parameters
    if(!verify())
    {
        qint64 elapsedMs = timer.elapsed();
        logError("Installation parameters are not valid. Aborting the installation of the pipe.");
        logError("Check the logs for more information.");
        logError(QString("Installation failed after %1 ms").arg(elapsedMs));
        emit this->installationFinished();
        return false;
    }
    processEvents();
    log("Vericiation done, installing the tools");
    processEvents();

    /// Iterate over the selected components and install them one by one
    for(auto it : selectedComponents()) {

        log("Installing the component : \"" + it + "\"...");
        bool installResult = false;

        if(it == "Main prism plugin") {
            processEvents();
            installResult = install_MainPrismPlugin();
        }
        else if (it == "Save as script Maya") {
            processEvents();
            installResult = install_MayaSaveAs();
        }
        else if (it == "Shelf Maya") {
            processEvents();
            installResult = install_MayaShelf();
        }
        else if (it == "Maya Asset Browser") {
            processEvents();
            installResult = install_MayaAssetBrowser();
        }
        else if( it == "Maya shot manager") {
            processEvents();
            installResult = install_MayaShotManager();
        }
        else if (it == "Houdini Asset Browser") {
            processEvents();
            installResult = install_HoudiniAssetBrowser();
        }
        else if (it == "Houdini custom nodes") {
            processEvents();
            installResult = install_HoudiniCustomNodes();
        }
        else if (it == "Substance painter plugin") {
            processEvents();
            installResult = install_SubstancePrismPlugin();
        }
        else if (it == "Zbrush prim plugin") {
            processEvents();
            installResult = install_ZBrushPrismPlugin();
        }

        // Enregistrer le résultat de l'installation
        if(installResult) {
            m_successfulComponents.append(it);
            logSuccess("Component \"" + it + "\" installed successfully.");
        } else {
            m_failedComponents.append(it);
            logError("Failed to install component \"" + it + "\".");
        }
        processEvents();
    }


    if(!install_nameAndUsernamePrism()) {
        m_failedComponents.append("Prism Name and username");
        logError("Failed to install component \"Prism Name and username\".");
    }
    else {
        m_successfulComponents.append(("\"Prism Name and username\""));
    }


    // Afficher le résumé des installations
    log("=== Installation Summary ===");



    if(!m_successfulComponents.isEmpty()) {
        logSuccess(QString("Successfully installed (%1 components):").arg(m_successfulComponents.size()));
        for(const QString& component : m_successfulComponents) {
            logSuccess("  ✓ " + component);
        }
    }
    
    if(!m_failedComponents.isEmpty()) {
        logError(QString("Failed to install (%1 components):").arg(m_failedComponents.size()));
        for(const QString& component : m_failedComponents) {
            logError("  ✗ " + component);
        }
    }
    
    // Calculer et afficher le temps total d'installation
    qint64 elapsedMs = timer.elapsed();
    double elapsedSeconds = elapsedMs / 1000.0;
    
    bool hasFailures = !m_failedComponents.isEmpty();
    QString completionMessage;
    
    if (elapsedMs < 1000) {
        completionMessage = QString("Installation completed in %1 ms").arg(elapsedMs);
    } else if (elapsedSeconds < 60) {
        completionMessage = QString("Installation completed in %1 seconds").arg(elapsedSeconds, 0, 'f', 2);
    } else {
        int minutes = static_cast<int>(elapsedSeconds / 60);
        double remainingSeconds = elapsedSeconds - (minutes * 60);
        completionMessage = QString("Installation completed in %1m %2s").arg(minutes).arg(remainingSeconds, 0, 'f', 1);
    }
    
    if(hasFailures) {
        completionMessage += QString(" (%1 successful, %2 failed)")
                            .arg(m_successfulComponents.size())
                            .arg(m_failedComponents.size());
        logError(completionMessage);
    } else {
        completionMessage += QString(" (all %1 components successful)")
                            .arg(m_successfulComponents.size());
        logSuccess(completionMessage);
    }

    emit this->installationFinished();
    return m_failedComponents.isEmpty();
}

bool InstallProcessTools::verify()
{
    processEvents();

    /// Check if the paths for the Maya path is valid
    QString mayaPath = SoftwareHelpers::getMayaPath();
    if( mayaPath == "" || !FileHelper::DirExists(mayaPath) )  {
        logError("Imporssible to find the path to the maya sofware.");
        return false;
    }

    /// Check if the paths for the Houdini path is valid
    QString houdiniPath = SoftwareHelpers::getHoudiniPath();
    if( houdiniPath == "" || !FileHelper::DirExists(houdiniPath) )  {
        logError("Imporssible to find the path to the Houdini sofware.");
        return false;
    }

    /// Check if the paths for the Zbrush path is valid
    QString zbrushPath = SoftwareHelpers::getZbrushPath();
    if( zbrushPath == "" || !FileHelper::DirExists(zbrushPath) )  {
        logError("Imporssible to find the path to the Zbrush sofware.");
        return false;
    }

    /// Check if the paths for the Substance Painter path is valid
    QString substancePainterPath = SoftwareHelpers::getSubstancePainterPath();
    if( substancePainterPath == "" || !FileHelper::DirExists(substancePainterPath) )  {
        logError("Imporssible to find the path to the Substance Painter sofware.");
        return false;
    }

    /// Check if the paths for the Prism path is valid
    QString prismPath = SoftwareHelpers::getPrismPath();
    if( prismPath == "" || !FileHelper::DirExists(prismPath) )  {
        logError("Imporssible to find the path to the Prism sofware.");
        return false;
    }

    /// Check if the paths for the preferences are valid
    QString mayaPrefsPath = SoftwareHelpers::getMayaPrefsPath();
    if( mayaPrefsPath == "" || !FileHelper::DirExists(mayaPrefsPath) )  {
        logError("Imporssible to find the path to the maya preferences.");
        return false;
    }

    QString houdiniPrefsPath = SoftwareHelpers::getHoudiniPrefsPath();
    if( houdiniPrefsPath == "" || !FileHelper::DirExists(houdiniPrefsPath) )  {
        logError("Imporssible to find the path to the Houdini preferences.");
        return false;
    }


    /// Check if there is a username
    if(username().isEmpty()) {
        logError("The username is empty. Please provide a valid username.");
        return false;
    }

    /// Check if there is an abreviation
    if(abreviation().isEmpty()) {
        logError("The abreviation is empty. Please provide a valid abreviation.");
        return false;
    }

    return true;
}

bool InstallProcessTools::install_MainPrismPlugin()
{
    QString prism_path = SoftwareHelpers::getPrismPath();
    QString prism_prefs_path = SoftwareHelpers::getPrismPrefsPath();

    QString prism_plugins_path = FileHelper::JoinPath(prism_path, "Plugins/Custom");
    if(!FileHelper::DirExists(prism_plugins_path)) {
        logError("The path to the prism plugins is not valid : " + prism_plugins_path);
        return false;
    }

    
    QString templatePath = FileHelper::GetResourcesPath();
    QString rootRepoPath = FileHelper::CdUp(templatePath, 2);
    QString pipeline_plugin_source = FileHelper::JoinPath(rootRepoPath, "prism");

    QString badger_pipeline_path = FileHelper::JoinPath(prism_plugins_path, "Badger_Pipeline");
    if(FileHelper::DirExists(badger_pipeline_path)) {
        /// We remove the existing Badger_Pipeline folder if it exists and replace it with the new one
        if(!FileHelper::DeleteDir(badger_pipeline_path)) {
            logError("Failed to remove the existing Badger_Pipeline directory: " + badger_pipeline_path);
            return false;
        }

        log("Removed the existing Badger_Pipeline directory: " + badger_pipeline_path);
        processEvents();
    }




    /// Check if the pipeline path contains a "Badger_Pipeline" folder
    if(!FileHelper::DirExists(pipeline_plugin_source)) {
        logError("The path to the prism plugin source is not valid : " + pipeline_plugin_source);
        return false;
    }

    /// Copy the prism plugin to the prism plugins folder recursively
    if(!copyFolderRecursive(pipeline_plugin_source, prism_plugins_path)) {
        logError("Failed to copy the prism plugin from : " + pipeline_plugin_source + " to " + prism_plugins_path);
        return false;
    }

    return true;
}





bool InstallProcessTools::install_SubstancePrismPlugin()
{
    QString substance_path = SoftwareHelpers::getSubstancePainterPath();
    QString prism_path = SoftwareHelpers::getPrismPath();

    return true;
}

bool InstallProcessTools::install_ZBrushPrismPlugin()
{
    QString zbrush_path = SoftwareHelpers::getZbrushPath();


    return true;
}

bool InstallProcessTools::install_MayaSaveAs()
{
    QString maya_prefs_path = SoftwareHelpers::getMayaPrefsPath();

    QString maya_scripts_path = FileHelper::JoinPath(maya_prefs_path , "scripts");
    QString maya_scripts_path_SaveAs = FileHelper::JoinPath(maya_scripts_path , "SaveAs");

    /// Check if the maya scripts path exists, if not create it
    if(!FileHelper::DirExists(maya_scripts_path)) {
        if(!QDir().mkpath(maya_scripts_path)) {
            logError("Failed to create the Maya scripts directory: " + maya_scripts_path);
            return false;
        }
    }
    else {
        /// We remove the existing SaveAs folder if it exists and replace it with the new one
        if(FileHelper::DirExists(maya_scripts_path_SaveAs)) {
            QDir dir(maya_scripts_path_SaveAs);
            if(!dir.removeRecursively()) {
                logError("Failed to remove the existing Maya SaveAs directory: " + maya_scripts_path_SaveAs);
                return false;
            }

            log("Removed the existing Maya SaveAs directory: " + maya_scripts_path_SaveAs);
            processEvents();

            /// Create the SaveAs folder
            if(!QDir().mkpath(maya_scripts_path_SaveAs)) {
                logError("Failed to create the Maya SaveAs directory: " + maya_scripts_path_SaveAs);
                return false;
            }

        }
    }

    QString templatePath = FileHelper::GetResourcesPath();
    QString rootRepoPath = FileHelper::CdUp(templatePath, 2);
    QString maya_scripts_path_template = FileHelper::JoinPath(rootRepoPath, "maya/scripts");

    /// Check if the maya_scripts_path contains a "SaveAs" folder
    if(!FileHelper::DirExists(maya_scripts_path_template)) {
        logError("The path to the maya scripts is not valid : " + maya_scripts_path_template);
        return false;
    }

    QString saveAsFolderPath = FileHelper::JoinPath(maya_scripts_path_template, "SaveAs");
    if(!FileHelper::DirExists(saveAsFolderPath)) {
        logError("The path to the Maya SaveAs folder is not valid : " + saveAsFolderPath);
        return false;
    }





    /// Copy the SaveAs folder to the Maya scripts folder recursively
    if(!copyFolderRecursive(saveAsFolderPath, maya_scripts_path_SaveAs)) {
        logError("Failed to copy the SaveAs folder from : " + saveAsFolderPath + " to " + maya_scripts_path);
        return false;
    }

    return true;
}

bool InstallProcessTools::install_MayaShelf()
{
    QString maya_prefs_path = SoftwareHelpers::getMayaPrefsPath();


    return true;
}



bool InstallProcessTools::install_MayaAssetBrowser()
{
    QString maya_prefs_path = SoftwareHelpers::getMayaPrefsPath();
    QString script_path = FileHelper::JoinPath(maya_prefs_path , "scripts");

    // Check if there is a "asset_browser_window" folder, if not create it
    QString asset_browser_path = FileHelper::JoinPath(script_path, "asset_browser_window");
    if(!FileHelper::DirExists(asset_browser_path)) {
        if(!QDir().mkpath(asset_browser_path)) {
            logError("Failed to create the Maya asset_browser_window directory: " + asset_browser_path);
            return false;
        }
    }
    else {
        /// We remove the existing asset_browser_window folder if it exists and replace it with the new one
        if(FileHelper::DirExists(asset_browser_path)) {
            QDir dir(asset_browser_path);
            if(!dir.removeRecursively()) {
                logError("Failed to remove the existing Maya asset_browser_window directory: " + asset_browser_path);
                return false;
            }

            log("Removed the existing Maya asset_browser_window directory: " + asset_browser_path);
            processEvents();

            /// Create the asset_browser_window folder
            if(!QDir().mkpath(asset_browser_path)) {
                logError("Failed to create the Maya asset_browser_window directory: " + asset_browser_path);
                return false;
            }

        }
    }


    QString templatePath = FileHelper::GetResourcesPath();
    QString rootRepoPath = FileHelper::CdUp(templatePath, 2);
    QString maya_asset_browser_template = FileHelper::JoinPath(rootRepoPath, "maya/scripts/asset_browser_window");

    /// Check if the maya_asset_browser_template path exists
    if(!FileHelper::DirExists(maya_asset_browser_template)) {
        logError("The path to the maya asset_browser_window is not valid : " + maya_asset_browser_template);
        return false;
    }

    /// Copy the asset_browser_window folder to the Maya scripts folder recursively
    if(!copyFolderRecursive(maya_asset_browser_template, asset_browser_path)) {
        logError("Failed to copy the asset_browser_window folder from : " + maya_asset_browser_template + " to " + asset_browser_path);
        return false;
    }


    log("Maya prefs path: " + maya_prefs_path);
    return true;
}

bool InstallProcessTools::install_MayaShotManager()
{
    QString maya_prefs_path = SoftwareHelpers::getMayaPrefsPath();

    QString shot_manager_path = FileHelper::JoinPath(maya_prefs_path, "scripts/shot_manager");
    // Check if the shot_manager_path exists, if not create it
    if(!FileHelper::DirExists(shot_manager_path)) {
        if(!QDir().mkpath(shot_manager_path)) {
            logError("Failed to create the Maya shot_manager directory: " + shot_manager_path);
            return false;
        }
    }
    else {
        /// We remove the existing shot_manager folder if it exists and replace it with the new one
        if(FileHelper::DirExists(shot_manager_path)) {
            QDir dir(shot_manager_path);
            if(!dir.removeRecursively()) {
                logError("Failed to remove the existing Maya shot_manager directory: " + shot_manager_path);
                return false;
            }

            log("Removed the existing Maya shot_manager directory: " + shot_manager_path);
            processEvents();

            /// Create the shot_manager folder
            if(!QDir().mkpath(shot_manager_path)) {
                logError("Failed to create the Maya shot_manager directory: " + shot_manager_path);
                return false;
            }

        }
    }

    QString templatePath = FileHelper::GetResourcesPath();
    QString rootRepoPath = FileHelper::CdUp(templatePath, 2);
    QString maya_shot_manager_template = FileHelper::JoinPath(rootRepoPath, "maya/scripts/shot_manager");
    /// Check if the maya_shot_manager_template path exists
    if(!FileHelper::DirExists(maya_shot_manager_template)) {
        logError("The path to the maya shot_manager is not valid : " + maya_shot_manager_template);
        return false;
    }

    /// Copy the shot_manager folder to the Maya scripts folder recursively
    if(!copyFolderRecursive(maya_shot_manager_template, shot_manager_path)) {
        logError("Failed to copy the shot_manager folder from : " + maya_shot_manager_template + " to " + shot_manager_path);
        return false;
    }
    


    return true;
}



bool InstallProcessTools::install_HoudiniAssetBrowser()
{
    QString houdini_prefs_path = SoftwareHelpers::getHoudiniPrefsPath();
    houdini_prefs_path = FileHelper::JoinPath(houdini_prefs_path , "python_panels");

    // If the folder does not exist, we create it
    if(!FileHelper::DirExists(houdini_prefs_path)) {
        if(!QDir().mkpath(houdini_prefs_path)) {
            logError("Failed to create the Houdini python_panels directory: " + houdini_prefs_path);
            return false;
        }
    }

    QString templatePath = FileHelper::GetResourcesPath();
    templatePath = FileHelper::CdUp(templatePath, 2);
    templatePath = FileHelper::JoinPath(templatePath, "houdini/asset_browser_window");

    /// Check if the path exists, retur if false
    if(!FileHelper::DirExists(templatePath)) {
        logError("The path to the houdini asset browser is not valid : " + templatePath);
        return false;
    }

    /// Files to
    QStringList filesToCopy = {
        "Bp_AssetBrowser.pypanel",
        "Bp_Install.pypanel"
    };
    for(auto it : filesToCopy) {
        copyFile(templatePath + "/" + it , houdini_prefs_path + "/" + it );
    }

    
    return true;
}

bool InstallProcessTools::install_HoudiniCustomNodes()
{
    QString houdini_prefs_path = SoftwareHelpers::getHoudiniPrefsPath();
    // @todo Voir avec romain si on met dans le otls, ou dans le serveur. 
    // Pour l'instant on met dans le otls

    // otls
    if(true) {
        QString houdini_otls_path = FileHelper::JoinPath(houdini_prefs_path , "otls");
        // Check if the houdini otls path exists, if not create it
        if(!FileHelper::DirExists(houdini_otls_path)) {
            if(!QDir().mkpath(houdini_otls_path)) {
                logError("Failed to create the Houdini otls directory: " + houdini_otls_path);
                return false;
            }
        }

        QString templatePath = FileHelper::GetResourcesPath();
        QString rootRepoPath = FileHelper::CdUp(templatePath, 2);
        QString houdini_otls_path_template = FileHelper::JoinPath(rootRepoPath, "houdini/nodes/");

        /// Copy the file "lop_Thomas.Bp_AssetReference.1.0.hdanc"
        /// Copy the file "lop_Thomas.BP_Export.1.0.hdanc"
        QStringList filesToCopy = {
            "lop_Thomas.Bp_AssetReference.1.0.hdanc",
            "lop_Thomas.BP_Export.1.0.hdanc",
            "lop_Thomas.BP_Anim_Import.1.0.hdanc"
        };
        for(auto it : filesToCopy) {
            copyFile(houdini_otls_path_template + "/" + it , houdini_otls_path + "/" + it );
        }

    }
    // serveur
    else {
    }

    return true;
}

bool InstallProcessTools::install_nameAndUsernamePrism()
{
    QString prism_prefs_path = SoftwareHelpers::getPrismPrefsPath();

    QJsonObject obj = FileHelper::GetJsonObjectFromFile(prism_prefs_path);
    if(obj.isEmpty()) {
        logError("Failed to read the Prism preferences file: " + prism_prefs_path);
        return false;
    }

    // We want to update the obj["globals"]["username"] and obj["globals"]["username_abbreviation"]
    QJsonObject globalsObj = obj.value("globals").toObject();
    globalsObj["username"] = username();
    globalsObj["username_abbreviation"] = abreviation();
    obj["globals"] = globalsObj;

    if(!FileHelper::WriteJsonObjectToFile(prism_prefs_path, obj)) {
        logError("Failed to write the updated Prism preferences file: " + prism_prefs_path);
        return false;
    }

    return true;
}

QString InstallProcessTools::abreviation() const
{
    return m_abreviation;
}

void InstallProcessTools::setAbreviation(const QString &newAbreviation)
{
    m_abreviation = newAbreviation;
}

QString InstallProcessTools::username() const
{
    return m_username;
}

void InstallProcessTools::setUsername(const QString &newUsername)
{
    m_username = newUsername;
}

bool InstallProcessTools::copyFile(const QString& sourcePath, const QString& destPath)
{
    if(!FileHelper::FileExists(sourcePath)) {
        logError("Source file does not exist: " + sourcePath);
        return false;
    }

    /// If the destination file already exists, we remove it first
    if(FileHelper::FileExists(destPath)) {
        if(!QFile::remove(destPath)) {
            logError("Failed to remove existing destination file: " + destPath);
            return false;
        }
        log("Removed existing destination file: " + destPath);
        processEvents();
    }


    if(!FileHelper::CopyFile(sourcePath, destPath)) {
        logError("Failed to copy file from " + sourcePath + " to " + destPath);
        return false;
    }
    processEvents();
    log("Copied file from " + sourcePath + " to " + destPath);
    return true;
}


bool InstallProcessTools::copyFolderRecursive(const QString &sourcePath, const QString &destPath)
{
    QDir sourceDir(sourcePath);
    if(!sourceDir.exists()) {
        logError("Source directory does not exist: " + sourcePath);
        return false;
    }

    QDir destDir(destPath);
    if(!destDir.exists()) {
        if(!destDir.mkpath(destPath)) {
            logError("Failed to create destination directory: " + destPath);
            return false;
        }
    }


    QFileInfoList entries = sourceDir.entryInfoList(QDir::NoDotAndDotDot | QDir::AllEntries);
    for(const QFileInfo &entry : entries) {
        QString srcFilePath = entry.absoluteFilePath();
        QString destFilePath = FileHelper::JoinPath(destPath, entry.fileName());

        if(entry.isDir()) {
            // Recursively copy subdirectory
            if(!copyFolderRecursive(srcFilePath, destFilePath)) {
                return false;
            }
        } else {
            // Copy file
            if(!FileHelper::CopyFile(srcFilePath, destFilePath)) {
                logError("Failed to copy file from " + srcFilePath + " to " + destFilePath);
                return false;
            }
            log("Copied file from " + srcFilePath + " to " + destFilePath);
        }
        processEvents();
    }

    log("Copied folder from " + sourcePath + " to " + destPath);
    return true;
}
