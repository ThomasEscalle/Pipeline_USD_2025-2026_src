
#include "FileHelper.h"
#include <windows.h>
#include <filesystem>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <regex>
#include <iomanip>
#include <ctime>
#include <random>
#include <shlobj.h>

namespace fs = std::filesystem;

// File existence and information
bool FileHelper::fileExists(const std::string& filePath) {
    return fs::exists(filePath) && fs::is_regular_file(filePath);
}

bool FileHelper::directoryExists(const std::string& dirPath) {
    return fs::exists(dirPath) && fs::is_directory(dirPath);
}

bool FileHelper::isFile(const std::string& path) {
    return fs::exists(path) && fs::is_regular_file(path);
}

bool FileHelper::isDirectory(const std::string& path) {
    return fs::exists(path) && fs::is_directory(path);
}

bool FileHelper::isEmpty(const std::string& path) {
    if (!fs::exists(path)) return true;
    
    if (fs::is_directory(path)) {
        return fs::directory_iterator(path) == fs::directory_iterator{};
    } else if (fs::is_regular_file(path)) {
        return fs::file_size(path) == 0;
    }
    return false;
}

size_t FileHelper::getFileSize(const std::string& filePath) {
    if (!fileExists(filePath)) return 0;
    return fs::file_size(filePath);
}

std::string FileHelper::getFileExtension(const std::string& filePath) {
    fs::path path(filePath);
    return path.extension().string();
}

std::string FileHelper::getFileName(const std::string& filePath) {
    fs::path path(filePath);
    return path.filename().string();
}

std::string FileHelper::getDirectoryName(const std::string& path) {
    fs::path p(path);
    return p.parent_path().string();
}

std::string FileHelper::getAbsolutePath(const std::string& path) {
    return fs::absolute(path).string();
}

// File operations
bool FileHelper::createFile(const std::string& filePath) {
    try {
        std::ofstream file(filePath);
        return file.good();
    } catch (...) {
        return false;
    }
}

bool FileHelper::deleteFile(const std::string& filePath) {
    try {
        return fs::remove(filePath);
    } catch (...) {
        return false;
    }
}

bool FileHelper::copyFile(const std::string& source, const std::string& destination) {
    try {
        return fs::copy_file(source, destination, fs::copy_options::overwrite_existing);
    } catch (...) {
        return false;
    }
}

bool FileHelper::moveFile(const std::string& source, const std::string& destination) {
    try {
        fs::rename(source, destination);
        return true;
    } catch (...) {
        return false;
    }
}

bool FileHelper::renameFile(const std::string& oldPath, const std::string& newPath) {
    return moveFile(oldPath, newPath);
}

// Directory operations
bool FileHelper::createDirectory(const std::string& dirPath) {
    try {
        return fs::create_directory(dirPath);
    } catch (...) {
        return false;
    }
}

bool FileHelper::createDirectoryRecursive(const std::string& dirPath) {
    try {
        return fs::create_directories(dirPath);
    } catch (...) {
        return false;
    }
}

bool FileHelper::deleteDirectory(const std::string& dirPath) {
    try {
        return fs::remove(dirPath);
    } catch (...) {
        return false;
    }
}

bool FileHelper::deleteDirectoryRecursive(const std::string& dirPath) {
    try {
        return fs::remove_all(dirPath) > 0;
    } catch (...) {
        return false;
    }
}

bool FileHelper::copyDirectory(const std::string& source, const std::string& destination) {
    try {
        fs::copy(source, destination, fs::copy_options::recursive | fs::copy_options::overwrite_existing);
        return true;
    } catch (...) {
        return false;
    }
}

bool FileHelper::moveDirectory(const std::string& source, const std::string& destination) {
    try {
        fs::rename(source, destination);
        return true;
    } catch (...) {
        return false;
    }
}

// File content operations
std::string FileHelper::readTextFile(const std::string& filePath) {
    std::ifstream file(filePath);
    if (!file.is_open()) return "";
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

std::vector<std::string> FileHelper::readTextFileLines(const std::string& filePath) {
    std::vector<std::string> lines;
    std::ifstream file(filePath);
    if (!file.is_open()) return lines;
    
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

bool FileHelper::writeTextFile(const std::string& filePath, const std::string& content) {
    try {
        std::ofstream file(filePath);
        if (!file.is_open()) return false;
        file << content;
        return file.good();
    } catch (...) {
        return false;
    }
}

bool FileHelper::writeTextFileLines(const std::string& filePath, const std::vector<std::string>& lines) {
    try {
        std::ofstream file(filePath);
        if (!file.is_open()) return false;
        
        for (size_t i = 0; i < lines.size(); ++i) {
            file << lines[i];
            if (i < lines.size() - 1) file << "\n";
        }
        return file.good();
    } catch (...) {
        return false;
    }
}

bool FileHelper::appendToTextFile(const std::string& filePath, const std::string& content) {
    try {
        std::ofstream file(filePath, std::ios::app);
        if (!file.is_open()) return false;
        file << content;
        return file.good();
    } catch (...) {
        return false;
    }
}

std::vector<char> FileHelper::readBinaryFile(const std::string& filePath) {
    std::vector<char> data;
    std::ifstream file(filePath, std::ios::binary);
    if (!file.is_open()) return data;
    
    file.seekg(0, std::ios::end);
    size_t size = file.tellg();
    file.seekg(0, std::ios::beg);
    
    data.resize(size);
    file.read(data.data(), size);
    return data;
}

bool FileHelper::writeBinaryFile(const std::string& filePath, const std::vector<char>& data) {
    try {
        std::ofstream file(filePath, std::ios::binary);
        if (!file.is_open()) return false;
        file.write(data.data(), data.size());
        return file.good();
    } catch (...) {
        return false;
    }
}

// Directory listing
std::vector<std::string> FileHelper::listFiles(const std::string& dirPath, bool recursive) {
    std::vector<std::string> files;
    if (!directoryExists(dirPath)) return files;
    
    try {
        if (recursive) {
            for (const auto& entry : fs::recursive_directory_iterator(dirPath)) {
                if (entry.is_regular_file()) {
                    files.push_back(entry.path().string());
                }
            }
        } else {
            for (const auto& entry : fs::directory_iterator(dirPath)) {
                if (entry.is_regular_file()) {
                    files.push_back(entry.path().string());
                }
            }
        }
    } catch (...) {
        // Return empty vector on error
    }
    
    return files;
}

std::vector<std::string> FileHelper::listDirectories(const std::string& dirPath, bool recursive) {
    std::vector<std::string> directories;
    if (!directoryExists(dirPath)) return directories;
    
    try {
        if (recursive) {
            for (const auto& entry : fs::recursive_directory_iterator(dirPath)) {
                if (entry.is_directory()) {
                    directories.push_back(entry.path().string());
                }
            }
        } else {
            for (const auto& entry : fs::directory_iterator(dirPath)) {
                if (entry.is_directory()) {
                    directories.push_back(entry.path().string());
                }
            }
        }
    } catch (...) {
        // Return empty vector on error
    }
    
    return directories;
}

std::vector<std::string> FileHelper::listAll(const std::string& dirPath, bool recursive) {
    std::vector<std::string> entries;
    if (!directoryExists(dirPath)) return entries;
    
    try {
        if (recursive) {
            for (const auto& entry : fs::recursive_directory_iterator(dirPath)) {
                entries.push_back(entry.path().string());
            }
        } else {
            for (const auto& entry : fs::directory_iterator(dirPath)) {
                entries.push_back(entry.path().string());
            }
        }
    } catch (...) {
        // Return empty vector on error
    }
    
    return entries;
}

std::vector<std::string> FileHelper::findFiles(const std::string& dirPath, const std::string& pattern, bool recursive) {
    std::vector<std::string> matchingFiles;
    if (!directoryExists(dirPath)) return matchingFiles;
    
    try {
        std::regex regexPattern(pattern);
        
        if (recursive) {
            for (const auto& entry : fs::recursive_directory_iterator(dirPath)) {
                if (entry.is_regular_file()) {
                    std::string filename = entry.path().filename().string();
                    if (std::regex_match(filename, regexPattern)) {
                        matchingFiles.push_back(entry.path().string());
                    }
                }
            }
        } else {
            for (const auto& entry : fs::directory_iterator(dirPath)) {
                if (entry.is_regular_file()) {
                    std::string filename = entry.path().filename().string();
                    if (std::regex_match(filename, regexPattern)) {
                        matchingFiles.push_back(entry.path().string());
                    }
                }
            }
        }
    } catch (...) {
        // Return empty vector on error
    }
    
    return matchingFiles;
}

// Path operations
std::string FileHelper::combinePath(const std::string& path1, const std::string& path2) {
    fs::path p1(path1);
    fs::path p2(path2);
    return (p1 / p2).string();
}

std::string FileHelper::normalizePathSeparators(const std::string& path) {
    std::string normalized = path;
    std::replace(normalized.begin(), normalized.end(), '/', '\\');
    return normalized;
}

std::vector<std::string> FileHelper::splitPath(const std::string& path) {
    std::vector<std::string> parts;
    fs::path p(path);
    
    for (const auto& part : p) {
        if (part != "/" && part != "\\") {
            parts.push_back(part.string());
        }
    }
    
    return parts;
}

std::string FileHelper::getCurrentDirectory() {
    try {
        return fs::current_path().string();
    } catch (...) {
        return "";
    }
}

bool FileHelper::setCurrentDirectory(const std::string& dirPath) {
    try {
        fs::current_path(dirPath);
        return true;
    } catch (...) {
        return false;
    }
}

// File attributes and permissions
bool FileHelper::isReadOnly(const std::string& filePath) {
    if (!fileExists(filePath)) return false;
    
    DWORD attributes = GetFileAttributesA(filePath.c_str());
    return (attributes != INVALID_FILE_ATTRIBUTES) && (attributes & FILE_ATTRIBUTE_READONLY);
}

bool FileHelper::setReadOnly(const std::string& filePath, bool readOnly) {
    if (!fileExists(filePath)) return false;
    
    DWORD attributes = GetFileAttributesA(filePath.c_str());
    if (attributes == INVALID_FILE_ATTRIBUTES) return false;
    
    if (readOnly) {
        attributes |= FILE_ATTRIBUTE_READONLY;
    } else {
        attributes &= ~FILE_ATTRIBUTE_READONLY;
    }
    
    return SetFileAttributesA(filePath.c_str(), attributes) != 0;
}

bool FileHelper::isHidden(const std::string& filePath) {
    if (!fs::exists(filePath)) return false;
    
    DWORD attributes = GetFileAttributesA(filePath.c_str());
    return (attributes != INVALID_FILE_ATTRIBUTES) && (attributes & FILE_ATTRIBUTE_HIDDEN);
}

bool FileHelper::setHidden(const std::string& filePath, bool hidden) {
    if (!fs::exists(filePath)) return false;
    
    DWORD attributes = GetFileAttributesA(filePath.c_str());
    if (attributes == INVALID_FILE_ATTRIBUTES) return false;
    
    if (hidden) {
        attributes |= FILE_ATTRIBUTE_HIDDEN;
    } else {
        attributes &= ~FILE_ATTRIBUTE_HIDDEN;
    }
    
    return SetFileAttributesA(filePath.c_str(), attributes) != 0;
}

// Utility functions
std::string FileHelper::getTempDirectory() {
    char tempPath[MAX_PATH];
    DWORD result = GetTempPathA(MAX_PATH, tempPath);
    if (result > 0 && result <= MAX_PATH) {
        return std::string(tempPath);
    }
    return "";
}

std::string FileHelper::createTempFile(const std::string& prefix, const std::string& extension) {
    std::string tempDir = getTempDirectory();
    if (tempDir.empty()) return "";
    
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1000, 9999);
    
    std::string tempFile;
    do {
        tempFile = combinePath(tempDir, prefix + std::to_string(dis(gen)) + extension);
    } while (fileExists(tempFile));
    
    if (createFile(tempFile)) {
        return tempFile;
    }
    return "";
}

std::string FileHelper::createTempDirectory(const std::string& prefix) {
    std::string tempDir = getTempDirectory();
    if (tempDir.empty()) return "";
    
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1000, 9999);
    
    std::string tempDirPath;
    do {
        tempDirPath = combinePath(tempDir, prefix + std::to_string(dis(gen)));
    } while (directoryExists(tempDirPath));
    
    if (createDirectory(tempDirPath)) {
        return tempDirPath;
    }
    return "";
}

bool FileHelper::isPathValid(const std::string& path) {
    if (path.empty()) return false;
    
    // Check for invalid characters
    const std::string invalidChars = "<>:\"|?*";
    for (char c : invalidChars) {
        if (path.find(c) != std::string::npos) {
            return false;
        }
    }
    
    // Check path length
    if (path.length() > MAX_PATH) return false;
    
    return true;
}

std::string FileHelper::sanitizeFileName(const std::string& fileName) {
    std::string sanitized = fileName;
    const std::string invalidChars = "<>:\"|?*\\/";
    
    for (char& c : sanitized) {
        if (invalidChars.find(c) != std::string::npos) {
            c = '_';
        }
    }
    
    return sanitized;
}

// File comparison
bool FileHelper::areFilesIdentical(const std::string& file1, const std::string& file2) {
    if (!fileExists(file1) || !fileExists(file2)) return false;
    
    if (getFileSize(file1) != getFileSize(file2)) return false;
    
    std::ifstream f1(file1, std::ios::binary);
    std::ifstream f2(file2, std::ios::binary);
    
    if (!f1.is_open() || !f2.is_open()) return false;
    
    const size_t bufferSize = 4096;
    char buffer1[bufferSize];
    char buffer2[bufferSize];
    
    while (f1.read(buffer1, bufferSize) && f2.read(buffer2, bufferSize)) {
        if (f1.gcount() != f2.gcount()) return false;
        if (std::memcmp(buffer1, buffer2, f1.gcount()) != 0) return false;
    }
    
    return f1.gcount() == f2.gcount();
}

std::string FileHelper::calculateFileHash(const std::string& filePath) {
    if (!fileExists(filePath)) return "";
    
    // Simple hash implementation using std::hash
    auto data = readBinaryFile(filePath);
    if (data.empty()) return "";
    
    std::hash<std::string> hasher;
    std::string dataStr(data.begin(), data.end());
    size_t hashValue = hasher(dataStr);
    
    std::stringstream ss;
    ss << std::hex << hashValue;
    return ss.str();
}

// File time operations
std::string FileHelper::getLastWriteTime(const std::string& filePath) {
    if (!fileExists(filePath)) return "";
    
    try {
        auto ftime = fs::last_write_time(filePath);
        auto sctp = std::chrono::time_point_cast<std::chrono::system_clock::duration>(
            ftime - fs::file_time_type::clock::now() + std::chrono::system_clock::now());
        auto time_t = std::chrono::system_clock::to_time_t(sctp);
        
        std::stringstream ss;
        ss << std::put_time(std::localtime(&time_t), "%Y-%m-%d %H:%M:%S");
        return ss.str();
    } catch (...) {
        return "";
    }
}

std::string FileHelper::getCreationTime(const std::string& filePath) {
    if (!fileExists(filePath)) return "";
    
    HANDLE hFile = CreateFileA(filePath.c_str(), GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE) return "";
    
    FILETIME creationTime;
    if (GetFileTime(hFile, &creationTime, NULL, NULL)) {
        CloseHandle(hFile);
        
        SYSTEMTIME sysTime;
        FileTimeToSystemTime(&creationTime, &sysTime);
        
        std::stringstream ss;
        ss << sysTime.wYear << "-" << std::setfill('0') << std::setw(2) << sysTime.wMonth 
           << "-" << std::setfill('0') << std::setw(2) << sysTime.wDay
           << " " << std::setfill('0') << std::setw(2) << sysTime.wHour
           << ":" << std::setfill('0') << std::setw(2) << sysTime.wMinute
           << ":" << std::setfill('0') << std::setw(2) << sysTime.wSecond;
        return ss.str();
    }
    
    CloseHandle(hFile);
    return "";
}

std::string FileHelper::getLastAccessTime(const std::string& filePath) {
    if (!fileExists(filePath)) return "";
    
    HANDLE hFile = CreateFileA(filePath.c_str(), GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE) return "";
    
    FILETIME accessTime;
    if (GetFileTime(hFile, NULL, &accessTime, NULL)) {
        CloseHandle(hFile);
        
        SYSTEMTIME sysTime;
        FileTimeToSystemTime(&accessTime, &sysTime);
        
        std::stringstream ss;
        ss << sysTime.wYear << "-" << std::setfill('0') << std::setw(2) << sysTime.wMonth 
           << "-" << std::setfill('0') << std::setw(2) << sysTime.wDay
           << " " << std::setfill('0') << std::setw(2) << sysTime.wHour
           << ":" << std::setfill('0') << std::setw(2) << sysTime.wMinute
           << ":" << std::setfill('0') << std::setw(2) << sysTime.wSecond;
        return ss.str();
    }
    
    CloseHandle(hFile);
    return "";
}

bool FileHelper::setLastWriteTime(const std::string& filePath, const std::string& timeStr) {
    if (!fileExists(filePath)) return false;
    
    try {
        return true;
    } catch (...) {
        return false;
    }
}

