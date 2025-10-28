#include "FileHelper.h"

#include <QFile>
#include <QDir>
#include <QFileInfo>
#include <QDebug>
#include <QStandardPaths>
#include <QCoreApplication>
#include <QDirIterator>

/// Check if a given directory path exist
bool FileHelper::DirExists(const QString &path)
{
    QDir dir(path);
    return dir.exists();
}

/// Join two paths
QString FileHelper::JoinPath(const QString &path1, const QString &path2)
{
    QDir dir(path1);
    return dir.filePath(path2);
}

/// Create a directory from a given path
bool FileHelper::CreateDir(const QString &path)
{
    QDir dir;
    if(!dir.exists(path))
    {
        return dir.mkpath(path);
    }
    return true;
}

/// Write a text file
bool FileHelper::WriteFile(const QString &filePath, const QString &content)
{
    QFile file(filePath);
    if(!file.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        qDebug() << "Failed to open file for writing:" << filePath;
        return false;
    }

    QTextStream out(&file);
    out << content;
    file.flush();
    file.close();
    return true;
}

QString FileHelper::GetExecutablePath()
{
    return QCoreApplication::applicationDirPath();
}

QString FileHelper::GetResourcesPath()
{
    QDir exeDir = QDir(QCoreApplication::applicationDirPath());
    exeDir.cdUp();
    if(!exeDir.cd("resources")) {
        exeDir.cdUp();
        exeDir.cd("resources");
        if(!exeDir.cd("resources")) {
            exeDir.cdUp();
            exeDir.cd("resources");
            if(!exeDir.cd("resources")) {
                exeDir.cdUp();
                exeDir.cd("resources");
                if(!exeDir.cd("resources")) {
                    exeDir.cdUp();
                    exeDir.cd("resources");
                }
            }
        }
    }

    return exeDir.absolutePath();
}

bool FileHelper::CopyFile(const QString &sourcePath, const QString &destPath)
{
    QFileInfo checkFile(sourcePath);
    if(!checkFile.exists() || !checkFile.isFile()) {
        qDebug() << "Source file does not exist:" << sourcePath;
        return false;
    }

    QFile sourceFile(sourcePath);
    if(!sourceFile.copy(destPath)) {
        qDebug() << "Failed to copy file from" << sourcePath << "to" << destPath << ":" << sourceFile.errorString();
        return false;
    }

    return true;
}


QStringList FileHelper::GetAllFilesInFolder(const QString &folderPath)
{
    QStringList fileList;
    QDir dir(folderPath);
    if(!dir.exists()) {
        qDebug() << "Directory does not exist:" << folderPath;
        return fileList;
    }

    /// Using QDirIterator to list files (non-recursive)
    QDirIterator it(folderPath, QDir::Files | QDir::NoSymLinks);
    while(it.hasNext()) {
        fileList.append(it.next());
    }
    return fileList;
}

QStringList FileHelper::GetAllFoldersInFolder(const QString &folderPath)
{
    QStringList folderList;
    QDir dir(folderPath);
    if(!dir.exists()) {
        qDebug() << "Directory does not exist:" << folderPath;
        return folderList;
    }

    /// Using QDirIterator to list folders (non-recursive)
    QDirIterator it(folderPath, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
    while(it.hasNext()) {
        folderList.append(it.next());
    }
    return folderList;
}

QStringList FileHelper::GetAllFilesAndFoldersInFolder(const QString &folderPath)
{
    QStringList itemList;
    QDir dir(folderPath);
    if(!dir.exists()) {
        qDebug() << "Directory does not exist:" << folderPath;
        return itemList;
    }

    /// Using QDirIterator to list files and folders (non-recursive)
    QDirIterator it(folderPath, QDir::Files | QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
    while(it.hasNext()) {
        itemList.append(it.next());
    }
    return itemList;
}

QStringList FileHelper::GetAllFilesInFolderRecursive(const QString &folderPath)
{
    QStringList fileList;
    QDir dir(folderPath);
    if(!dir.exists()) {
        qDebug() << "Directory does not exist:" << folderPath;
        return fileList;
    }

    /// Using QDirIterator to list files (recursive)
    QDirIterator it(folderPath, QDir::Files | QDir::NoSymLinks, QDirIterator::Subdirectories);
    while(it.hasNext()) {
        fileList.append(it.next());
    }
    return fileList;
}

QStringList FileHelper::GetAllFoldersInFolderRecursive(const QString &folderPath)
{
    QStringList folderList;
    QDir dir(folderPath);
    if(!dir.exists()) {
        qDebug() << "Directory does not exist:" << folderPath;
        return folderList;
    }

    /// Using QDirIterator to list folders (recursive)
    QDirIterator it(folderPath, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks, QDirIterator::Subdirectories);
    while(it.hasNext()) {
        folderList.append(it.next());
    }
    return folderList;
}

QStringList FileHelper::GetAllFilesAndFoldersInFolderRecursive(const QString &folderPath)
{
    QStringList itemList;
    QDir dir(folderPath);
    if(!dir.exists()) {
        qDebug() << "Directory does not exist:" << folderPath;
        return itemList;
    }

    /// Using QDirIterator to list files and folders (recursive)
    QDirIterator it(folderPath, QDir::Files | QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks, QDirIterator::Subdirectories);
    while(it.hasNext()) {
        itemList.append(it.next());
    }
    return itemList;
}

QJsonObject FileHelper::GetJsonObjectFromFile(const QString &filePath)
{
    /// Open a json object from a file.
    QFile file(filePath);
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        qDebug() << "Failed to open file for reading:" << filePath;
        return QJsonObject();
    }
    QByteArray data = file.readAll();
    file.close();

    QJsonDocument doc = QJsonDocument::fromJson(data);
    if(doc.isNull() || !doc.isObject())
    {
        qDebug() << "Failed to parse JSON from file:" << filePath;
        return QJsonObject();
    }
    return doc.object();
}

bool FileHelper::WriteJsonObjectToFile(const QString &filePath, const QJsonObject &obj)
{
    QJsonDocument doc(obj);
    QByteArray data = doc.toJson();

    QFile file(filePath);
    if(!file.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        qDebug() << "Failed to open file for writing:" << filePath;
        return false;
    }

    qint64 bytesWritten = file.write(data);
    if(bytesWritten == -1)
    {
        qDebug() << "Failed to write JSON data to file:" << filePath;
        file.close();
        return false;
    }

    file.flush();
    file.close();
    return true;
}


QString FileHelper::GetFileNameFromPath(const QString &filePath)
{
    QFileInfo fileInfo(filePath);
    return fileInfo.fileName();
}

QString FileHelper::ReadFile(const QString &filePath)
{
    QFile file(filePath);
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        qDebug() << "Failed to open file for reading:" << filePath;
        return "";
    }

    QTextStream in(&file);
    QString content = in.readAll();
    file.close();
    return content;
}

bool FileHelper::ReadFile(const QString &filePath, QString &content)
{
    QFile file(filePath);
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        qDebug() << "Failed to open file for reading:" << filePath;
        return false;
    }

    QTextStream in(&file);
    content = in.readAll();
    file.close();
    return true;
}

QString FileHelper::CdUp(const QString &path, int levels)
{
    QDir dir(path);
    for(int i = 0; i < levels; ++i) {
        dir.cdUp();
    }
    return dir.absolutePath();
}

bool FileHelper::FileExists(const QString &path)
{
    QFileInfo checkFile(path);
    return checkFile.exists() && checkFile.isFile();
}

bool FileHelper::DeleteDir(const QString &path)
{
    QDir dir(path);
    if(!dir.exists()) {
        return true; // Directory does not exist, consider it deleted
    }
    return dir.removeRecursively();
}

bool FileHelper::DeleteFile(const QString &path)
{
    QFile file(path);
    if(!file.exists()) {
        return true; // File does not exist, consider it deleted
    }
    return file.remove();
}

bool FileHelper::ReplaceVariableInFile(const QString &filePath, const QString &variable, const QString &value)
{
    QString content;
    if(!ReadFile(filePath, content)) {
        qDebug() << "Failed to read file for variable replacement:" << filePath;
        return false;
    }

    content.replace(variable, value);

    if(!WriteFile(filePath, content)) {
        qDebug() << "Failed to write file after variable replacement:" << filePath;
        return false;
    }

    return true;
}

bool FileHelper::AppendLineToFile(const QString &filePath, const QString &line)
{
    QFile file(filePath);
    if(!file.open(QIODevice::Append | QIODevice::Text))
    {
        qDebug() << "Failed to open file for appending:" << filePath;
        return false;
    }

    QTextStream out(&file);
    out << line << "\n";
    file.flush();
    file.close();
    return true;
}