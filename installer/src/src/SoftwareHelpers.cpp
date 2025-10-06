#include "SoftwareHelpers.h"
#include <QString>
#include <QStringList>
#include <QMap>
#include <QVector>
#ifdef Q_OS_WIN
#include <windows.h>
#endif
#include <QDebug>
#include <QDir>
#include <QStandardPaths>
#include "FileHelper.h"


QString SoftwareHelpers::getMayaPath()
{
#ifdef Q_OS_WIN
    HKEY hKey;
    LONG result = RegOpenKeyExW(
        HKEY_LOCAL_MACHINE,
        L"SOFTWARE\\Autodesk\\Maya",
        0,
        KEY_READ | KEY_WOW64_64KEY,
        &hKey
    );
    if (result != ERROR_SUCCESS) return "";

    QStringList mayaVersions;
    DWORD index = 0;
    WCHAR subKeyName[256];
    DWORD subKeyLen = 256;
    while (RegEnumKeyExW(hKey, index, subKeyName, &subKeyLen, NULL, NULL, NULL, NULL) == ERROR_SUCCESS) {
        QString version = QString::fromWCharArray(subKeyName, subKeyLen);
        if (version.toInt()) mayaVersions << version;
        index++;
        subKeyLen = 256;
    }
    RegCloseKey(hKey);
    if (mayaVersions.isEmpty()) return "";

    QString validVersion = mayaVersions.last();
    QString installPathKey = QString("SOFTWARE\\Autodesk\\Maya\\%1\\Setup\\InstallPath").arg(validVersion);
    result = RegOpenKeyExW(
        HKEY_LOCAL_MACHINE,
        (LPCWSTR)installPathKey.utf16(),
        0,
        KEY_READ | KEY_WOW64_64KEY,
        &hKey
    );
    if (result != ERROR_SUCCESS) return "";

    WCHAR value[512];
    DWORD valueLen = sizeof(value);
    result = RegQueryValueExW(hKey, L"MAYA_INSTALL_LOCATION", NULL, NULL, (LPBYTE)value, &valueLen);
    RegCloseKey(hKey);
    if (result != ERROR_SUCCESS) return "";

    QString resultFinal = QString::fromWCharArray(value, valueLen / sizeof(WCHAR) - 1);
    resultFinal = resultFinal.replace("\\" , "/");
    return resultFinal;
#else
    return "";
#endif
}


/// @brief  Get the Maya preferences path
/// @note   On Windows, it's located in C:/Users/Username/Documents/maya/<version>
QString SoftwareHelpers::getMayaPrefsPath()
{
#ifdef Q_OS_WIN
    // Récupère le dossier Documents de l'utilisateur
    QString documentsPath = QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation);
    // Récupère la version Maya installée (utilise la même logique que getMayaPath)
    QString mayaVersion;
    {
        HKEY hKey;
        LONG result = RegOpenKeyExW(
            HKEY_LOCAL_MACHINE,
            L"SOFTWARE\\Autodesk\\Maya",
            0,
            KEY_READ | KEY_WOW64_64KEY,
            &hKey
        );
        if (result == ERROR_SUCCESS) {
            QStringList mayaVersions;
            DWORD index = 0;
            WCHAR subKeyName[256];
            DWORD subKeyLen = 256;
            while (RegEnumKeyExW(hKey, index, subKeyName, &subKeyLen, NULL, NULL, NULL, NULL) == ERROR_SUCCESS) {
                QString version = QString::fromWCharArray(subKeyName, subKeyLen);
                if (version.toInt()) mayaVersions << version;
                index++;
                subKeyLen = 256;
            }
            RegCloseKey(hKey);
            if (!mayaVersions.isEmpty()) mayaVersion = mayaVersions.last();
        }
    }
    if (documentsPath.isEmpty() || mayaVersion.isEmpty()) return "";
    // Construit le chemin des préférences Maya
    QString prefsPath = QString("%1/maya/%2").arg(documentsPath).arg(mayaVersion);
    return prefsPath.replace("\\", "/");
#else
    return "";
#endif
}

QString SoftwareHelpers::getHoudiniPath()
{
#ifdef Q_OS_WIN
    HKEY hKey;
    LONG result = RegOpenKeyExW(
        HKEY_LOCAL_MACHINE,
        L"SOFTWARE\\Side Effects Software\\Houdini",
        0,
        KEY_READ | KEY_WOW64_64KEY,
        &hKey
    );
    if (result != ERROR_SUCCESS) {
        qWarning("WARNING : Houdini n'est pas installé ou la clé de registre est manquante.");
        return "";
    }

    QMap<QString, QString> versions;
    DWORD index = 0;
    WCHAR valueName[256];
    DWORD valueNameLen = 256;
    BYTE valueData[512];
    DWORD valueDataLen = 512;
    DWORD type;
    while (true) {
        valueNameLen = 256;
        valueDataLen = 512;
        LONG enumResult = RegEnumValueW(hKey, index, valueName, &valueNameLen, NULL, &type, valueData, &valueDataLen);
        if (enumResult != ERROR_SUCCESS) break;
        QString name = QString::fromWCharArray(valueName, valueNameLen);
        if (name != "LicenseServer" && type == REG_SZ) {
            QString value = QString::fromWCharArray(reinterpret_cast<wchar_t*>(valueData), valueDataLen / sizeof(wchar_t) - 1);
            versions[name] = value;
        }
        index++;
    }
    RegCloseKey(hKey);

    if (!versions.isEmpty()) {
        // Trier les versions et prendre la plus récente
        QList<QString> keys = versions.keys();
        std::sort(keys.begin(), keys.end(), [](const QString& a, const QString& b) {
            QStringList va = a.split('.');
            QStringList vb = b.split('.');
            int len = std::min(va.size(), vb.size());
            for (int i = 0; i < len; ++i) {
                int ia = va[i].toInt();
                int ib = vb[i].toInt();
                if (ia != ib) return ia > ib;
            }
            return va.size() > vb.size();
        });
        QString latestVersion = keys.first();
        QString resultFinal = versions[latestVersion].replace("\\", "/");
        return resultFinal;
    }
    return "";
#else
    return "";
#endif
}

/// @brief  Get the Houdini preferences path
/// @note   On Windows, it's located in C:/Users/Username/Documents/houdini<version>
QString SoftwareHelpers::getHoudiniPrefsPath()
{
#ifdef Q_OS_WIN
    // Récupère le dossier Documents de l'utilisateur
    QString documentsPath = QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation);
    QString houdiniVersion;
    {
        HKEY hKey;
        LONG result = RegOpenKeyExW(
            HKEY_LOCAL_MACHINE,
            L"SOFTWARE\\Side Effects Software\\Houdini",
            0,
            KEY_READ | KEY_WOW64_64KEY,
            &hKey
        );
        if (result == ERROR_SUCCESS) {
            QList<QString> versions;
            DWORD index = 0;
            WCHAR valueName[256];
            DWORD valueNameLen = 256;
            BYTE valueData[512];
            DWORD valueDataLen = 512;
            DWORD type;
            while (true) {
                valueNameLen = 256;
                valueDataLen = 512;
                LONG enumResult = RegEnumValueW(hKey, index, valueName, &valueNameLen, NULL, &type, valueData, &valueDataLen);
                if (enumResult != ERROR_SUCCESS) break;
                QString name = QString::fromWCharArray(valueName, valueNameLen);
                if (name != "LicenseServer" && type == REG_SZ) {
                    versions.append(name);
                }
                index++;
            }
            RegCloseKey(hKey);
            if (!versions.isEmpty()) {
                std::sort(versions.begin(), versions.end(), [](const QString& a, const QString& b) {
                    QStringList va = a.split('.');
                    QStringList vb = b.split('.');
                    int len = std::min(va.size(), vb.size());
                    for (int i = 0; i < len; ++i) {
                        int ia = va[i].toInt();
                        int ib = vb[i].toInt();
                        if (ia != ib) return ia > ib;
                    }
                    return va.size() > vb.size();
                });
                houdiniVersion = versions.first();
            }
        }
    }
    if (documentsPath.isEmpty() || houdiniVersion.isEmpty()) return "";
    // Ne garder que les deux premiers segments de la version (ex: 20.5)
    QStringList versionParts = houdiniVersion.split('.');
    QString shortVersion;
    if (versionParts.size() >= 2) {
        shortVersion = versionParts[0] + "." + versionParts[1];
    } else {
        shortVersion = houdiniVersion;
    }
    // Construit le chemin des préférences Houdini
    QString prefsPath = QString("%1/houdini%2").arg(documentsPath).arg(shortVersion);
    return prefsPath.replace("\\", "/");
#else
    return "";
#endif
}

QString SoftwareHelpers::getZbrushPath()
{
#ifdef Q_OS_WIN
    QVector<QString> zPaths;
    // Pixologic
    HKEY hKey;
    LONG result = RegOpenKeyExW(
        HKEY_LOCAL_MACHINE,
        L"SOFTWARE\\Pixologic",
        0,
        KEY_READ | KEY_WOW64_64KEY,
        &hKey
    );
    if (result == ERROR_SUCCESS) {
        DWORD idx = 0;
        WCHAR subKeyName[256];
        DWORD subKeyLen = 256;
        while (RegEnumKeyExW(hKey, idx, subKeyName, &subKeyLen, NULL, NULL, NULL, NULL) == ERROR_SUCCESS) {
            QString zVersion = QString::fromWCharArray(subKeyName, subKeyLen);
            HKEY zKey;
            QString zKeyPath = QString("SOFTWARE\\Pixologic\\%1").arg(zVersion);
            LONG res2 = RegOpenKeyExW(
                HKEY_LOCAL_MACHINE,
                (LPCWSTR)zKeyPath.utf16(),
                0,
                KEY_READ | KEY_WOW64_64KEY,
                &zKey
            );
            if (res2 == ERROR_SUCCESS) {
                WCHAR value[512];
                DWORD valueLen = sizeof(value);
                if (RegQueryValueExW(zKey, L"Location", NULL, NULL, (LPBYTE)value, &valueLen) == ERROR_SUCCESS) {
                    QString path = QString::fromWCharArray(value, valueLen / sizeof(WCHAR) - 1).replace("\\", "/");
                    zPaths.append(path);
                }
                RegCloseKey(zKey);
            }
            idx++;
            subKeyLen = 256;
        }
        RegCloseKey(hKey);
    }

    // Maxon
    result = RegOpenKeyExW(
        HKEY_LOCAL_MACHINE,
        L"SOFTWARE\\Maxon",
        0,
        KEY_READ | KEY_WOW64_64KEY,
        &hKey
    );
    if (result == ERROR_SUCCESS) {
        DWORD idx = 0;
        WCHAR subKeyName[256];
        DWORD subKeyLen = 256;
        while (RegEnumKeyExW(hKey, idx, subKeyName, &subKeyLen, NULL, NULL, NULL, NULL) == ERROR_SUCCESS) {
            QString zVersion = QString::fromWCharArray(subKeyName, subKeyLen);
            if (!zVersion.toLower().contains("zbrush")) {
                idx++;
                subKeyLen = 256;
                continue;
            }
            HKEY zKey;
            QString zKeyPath = QString("SOFTWARE\\Maxon\\%1").arg(zVersion);
            LONG res2 = RegOpenKeyExW(
                HKEY_LOCAL_MACHINE,
                (LPCWSTR)zKeyPath.utf16(),
                0,
                KEY_READ | KEY_WOW64_64KEY,
                &zKey
            );
            if (res2 == ERROR_SUCCESS) {
                WCHAR value[512];
                DWORD valueLen = sizeof(value);
                if (RegQueryValueExW(zKey, L"Location", NULL, NULL, (LPBYTE)value, &valueLen) == ERROR_SUCCESS) {
                    QString path = QString::fromWCharArray(value, valueLen / sizeof(WCHAR) - 1).replace("\\", "/");
                    zPaths.append(path);
                }
                RegCloseKey(zKey);
            }
            idx++;
            subKeyLen = 256;
        }
        RegCloseKey(hKey);
    }

    // Retourne le dernier chemin trouvé ou une chaîne vide
    return zPaths.isEmpty() ? "" : zPaths.last();
#else
    return "";
#endif
}

// Rechercher dans l'editeur de registre le chemin : HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Adobe Substance 3D Painter.exe, puis la valeur "Path"
QString SoftwareHelpers::getSubstancePainterPath()
{
#ifdef Q_OS_WIN
    HKEY hKey;
    LONG result = RegOpenKeyExW(
        HKEY_LOCAL_MACHINE,
        L"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\Adobe Substance 3D Painter.exe",
        0,
        KEY_READ | KEY_WOW64_64KEY,
        &hKey
    );
    if (result != ERROR_SUCCESS) return "";

    WCHAR value[512];
    DWORD valueLen = sizeof(value);
    result = RegQueryValueExW(hKey, L"Path", NULL, NULL, (LPBYTE)value, &valueLen);
    RegCloseKey(hKey);
    if (result != ERROR_SUCCESS) return "";

    QString resultFinal = QString::fromWCharArray(value, valueLen / sizeof(WCHAR) - 1);
    resultFinal = resultFinal.replace("\\" , "/");
    resultFinal = resultFinal.replace("\"", "");
    return resultFinal;
#else
    return "";
#endif
}

QString SoftwareHelpers::getSubstancePrefsPath()
{
    /// Prism prefs path is located in:
    /// Documents/Prism2/Prism.json
    /// Documents/Prism/Prism.json

    QString documentsPath = QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation).replace("\\", "/");
    QString substancePrefsPath =FileHelper::JoinPath( documentsPath , "Adobe/Adobe Substance 3D Painter");

    if(!FileHelper::DirExists(substancePrefsPath)) {
        if(!FileHelper::CreateDir(substancePrefsPath) ) {
            return "";
        }
    }

    return substancePrefsPath;
}



QString SoftwareHelpers::getPrismPath()
{
    /// Search for a folder named "Prism".
    /// THis sofware is not in the registry.
    /// So we want to scan the "Program Files" folders and "Program Files (x86)" folders.
    /// Than, we scan the root of each Disk (C:/, D:/, E:/, etc...) to find a folder named "Prism"
    /// If we find it, we return the path.

    QDir dir;
    QStringList foldersToScan;

    // Add the standard program files folders
    foldersToScan << QStandardPaths::writableLocation(QStandardPaths::ApplicationsLocation).replace("\\", "/");
    foldersToScan << QStandardPaths::writableLocation(QStandardPaths::HomeLocation).replace("\\", "/");
    foldersToScan << QStandardPaths::writableLocation(QStandardPaths::ApplicationsLocation).replace("\\", "/").replace(" (x86)", "");

    /// Add all the disks roots
    foreach (const QFileInfo &drive, QDir::drives()) {
        foldersToScan << drive.absolutePath().replace("\\", "/");
        foldersToScan << drive.absolutePath().replace("\\", "/") + "Program Files";
        foldersToScan << drive.absolutePath().replace("\\", "/") + "C:/Program Files (x86)";
    }

    // Scan the root of each disk
    for (auto it : foldersToScan) {
        // Check for prism in the folder
        QString prismPath = it + "/Prism";
        prismPath.replace("\\", "/");
        prismPath.replace("//" , "/");
        if (QDir(prismPath).exists()) {
            QString path = prismPath.replace("\\", "/");
            path = path.replace("//", "/");


            /// Check if there is a "Python311/Prism.exe" file in this folder
            if (QFile::exists(path + "/Python311/Prism.exe")) {
                return path;
            }
        }
        
        // Check for prism2 in the folder
        prismPath = it + "/Prism2";
        prismPath.replace("\\", "/");
        prismPath.replace("//" , "/");
        if (QDir(prismPath).exists()) {
            QString path = prismPath.replace("\\", "/");
            path = path.replace("//", "/");


            /// Check if there is a "Python311/Prism.exe" file in this folder
            if (QFile::exists(path + "/Python311/Prism.exe")) {
                return path;
            }
        }
    }

    return "";
}

QString SoftwareHelpers::getPrismPrefsPath()
{
    /// Prism prefs path is located in:
    /// Documents/Prism2/Prism.json
    /// Documents/Prism/Prism.json

    QString documentsPath = QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation).replace("\\", "/");
    QString prismPrefsPath = documentsPath + "/Prism2/Prism.json";
    if (QFile::exists(prismPrefsPath)) {
        return prismPrefsPath;
    }
    prismPrefsPath = documentsPath + "/Prism/Prism.json";
    if (QFile::exists(prismPrefsPath)) {
        return prismPrefsPath;
    }
    

    return "";
}
