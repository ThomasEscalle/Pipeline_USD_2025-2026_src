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
