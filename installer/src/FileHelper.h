

#pragma once
#include <string>
#include <vector>
#include <fstream>
#include <filesystem>

class FileHelper {
public:
    // File existence and information
    static bool fileExists(const std::string& filePath);
    static bool directoryExists(const std::string& dirPath);
    static bool isFile(const std::string& path);
    static bool isDirectory(const std::string& path);
    static bool isEmpty(const std::string& path);
    static size_t getFileSize(const std::string& filePath);
    static std::string getFileExtension(const std::string& filePath);
    static std::string getFileName(const std::string& filePath);
    static std::string getDirectoryName(const std::string& path);
    static std::string getAbsolutePath(const std::string& path);
    
    // File operations
    static bool createFile(const std::string& filePath);
    static bool deleteFile(const std::string& filePath);
    static bool copyFile(const std::string& source, const std::string& destination);
    static bool moveFile(const std::string& source, const std::string& destination);
    static bool renameFile(const std::string& oldPath, const std::string& newPath);
    
    // Directory operations
    static bool createDirectory(const std::string& dirPath);
    static bool createDirectoryRecursive(const std::string& dirPath);
    static bool deleteDirectory(const std::string& dirPath);
    static bool deleteDirectoryRecursive(const std::string& dirPath);
    static bool copyDirectory(const std::string& source, const std::string& destination);
    static bool moveDirectory(const std::string& source, const std::string& destination);
    
    // File content operations
    static std::string readTextFile(const std::string& filePath);
    static std::vector<std::string> readTextFileLines(const std::string& filePath);
    static bool writeTextFile(const std::string& filePath, const std::string& content);
    static bool writeTextFileLines(const std::string& filePath, const std::vector<std::string>& lines);
    static bool appendToTextFile(const std::string& filePath, const std::string& content);
    static std::vector<char> readBinaryFile(const std::string& filePath);
    static bool writeBinaryFile(const std::string& filePath, const std::vector<char>& data);
    
    // Directory listing
    static std::vector<std::string> listFiles(const std::string& dirPath, bool recursive = false);
    static std::vector<std::string> listDirectories(const std::string& dirPath, bool recursive = false);
    static std::vector<std::string> listAll(const std::string& dirPath, bool recursive = false);
    static std::vector<std::string> findFiles(const std::string& dirPath, const std::string& pattern, bool recursive = true);
    
    // Path operations
    static std::string combinePath(const std::string& path1, const std::string& path2);
    static std::string normalizePathSeparators(const std::string& path);
    static std::vector<std::string> splitPath(const std::string& path);
    static std::string getCurrentDirectory();
    static bool setCurrentDirectory(const std::string& dirPath);
    
    // File attributes and permissions
    static bool isReadOnly(const std::string& filePath);
    static bool setReadOnly(const std::string& filePath, bool readOnly);
    static bool isHidden(const std::string& filePath);
    static bool setHidden(const std::string& filePath, bool hidden);
    
    // Utility functions
    static std::string getTempDirectory();
    static std::string createTempFile(const std::string& prefix = "temp", const std::string& extension = ".tmp");
    static std::string createTempDirectory(const std::string& prefix = "temp");
    static bool isPathValid(const std::string& path);
    static std::string sanitizeFileName(const std::string& fileName);
    
    // File comparison
    static bool areFilesIdentical(const std::string& file1, const std::string& file2);
    static std::string calculateFileHash(const std::string& filePath);
    
    // File time operations
    static std::string getLastWriteTime(const std::string& filePath);
    static std::string getCreationTime(const std::string& filePath);
    static std::string getLastAccessTime(const std::string& filePath);
    static bool setLastWriteTime(const std::string& filePath, const std::string& timeStr);
};
