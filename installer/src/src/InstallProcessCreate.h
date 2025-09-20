#ifndef INSTALLPROCESSCREATE_H
#define INSTALLPROCESSCREATE_H

#include "InstallProcess.h"


/**
 * @brief The InstallProcessCreate class
 * Handles the installation process for creating a new project
 */
class InstallProcessCreate : public InstallProcess
{
    Q_OBJECT

public:
    explicit InstallProcessCreate(QObject *parent = nullptr);
    virtual ~InstallProcessCreate();

public:

    /// INSTALLATION MAIN LOOP
    bool install() override;

    /// @brief Verify the installation parameters (name, path, software found ...)
    /// @return true if all parameters are valid, false otherwise
    bool verify();

    /// @brief Create the project structure (folders, )
    bool createProjectStructure( const QString &fullProjectPath );

    /// @brief Fill the pipeline folder with the default files and folders
    bool fillPipelineFolder( const QString &pipelinePath );

public:

    QString projectName() const;
    void setProjectName(const QString &newProjectName);

    QString projectPath() const;
    void setProjectPath(const QString &newProjectPath);

private:

    bool createFolder(const QString& path, const QString& folderName);
    bool createReadmeFile(const QString& path, const QString& content);
    bool createEmptyJsonObjectFile(const QString& path);
    bool createEmptyJsonArrayFile(const QString& path);

    bool copyFile(const QString& sourcePath, const QString& destPath);
    bool copyAllContainedFilesToFolder(const QString& sourceFolder, const QString& destFolder);

    bool replaceInFile(const QString& filePath, const QString& placeholder, const QString& value);

private:
    QString m_projectName;
    QString m_projectPath;
};

#endif // INSTALLPROCESSCREATE_H
