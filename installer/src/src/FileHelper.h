#ifndef FILEHELPER_H
#define FILEHELPER_H

#include <QObject>
#include <QJsonObject>

class FileHelper : public QObject
{
    Q_OBJECT
public:

    /// Check if a given directory path exist
    static bool DirExists(const QString& path);
    static bool FileExists(const QString& path);
    /// Join two paths
    static QString JoinPath(const QString& path1, const QString& path2);

    /// Create a directory from a given path
    static bool CreateDir(const QString& path);
    static bool DeleteDir(const QString& path);

    /// Read the content of a text file
    static QString ReadFile(const QString& filePath);
    static bool ReadFile(const QString& filePath, QString& content);
    /// Write a text file
    static bool WriteFile(const QString& filePath, const QString& content);

    /// Get the path of the executable
    static QString GetExecutablePath();

    /// Get the path of the resources folder of the app (executable path/../resources)
    static QString GetResourcesPath();

    /// Copy a file from source to destination
    static bool CopyFile(const QString& sourcePath, const QString& destPath);

    /// Get the file name from a given path
    static QString GetFileNameFromPath(const QString& filePath);

    static QString CdUp(const QString& path, int levels=1);

    /// Get the list of all the files in a given folder (non recursive)
    static QStringList GetAllFilesInFolder(const QString& folderPath);
    
    /// Get the list of all the folders in a given folder (non recursive)   
    static QStringList GetAllFoldersInFolder(const QString& folderPath);
    
    /// Get the list of all the files and folders in a given folder (non recursive)
    static QStringList GetAllFilesAndFoldersInFolder(const QString& folderPath);
    
    /// Get the list of all the files in a given folder (recursive)
    static QStringList GetAllFilesInFolderRecursive(const QString& folderPath);

    /// Get the list of all the folders in a given folder (recursive)
    static QStringList GetAllFoldersInFolderRecursive(const QString& folderPath);

    /// Get the list of all the files and folders in a given folder (recursive)
    static QStringList GetAllFilesAndFoldersInFolderRecursive(const QString& folderPath);
    

    static QJsonObject GetJsonObjectFromFile(const QString& filePath);
    static bool WriteJsonObjectToFile(const QString& filePath, const QJsonObject& obj);


public:



};

#endif // FILEHELPER_H
