#include "src/MainWizard.h"

#include <QApplication>

#include "SoftwareHelpers.h"
#include "FileHelper.h"
#include <QDebug>
#include <QSysInfo>


#include <QProcess>
#include <QDebug>

// Fonction pour tuer une application par son nom (ex: "notepad.exe")
bool killApplication(const QString &appName) {
    /// Run  taskkill /F /IM Prism.exe
    ///
    QString program = "taskkill";
    QStringList arguments;
    arguments << "/F" << "/IM" << appName;
    QProcess process;
    process.start(program, arguments);
    process.waitForFinished();
    return process.exitCode() == 0;
}

bool resetResourcePath() {

    QString srcPath  = "D:/Pipeline_USD_2025-2026_src/resources/prism_title.png";
    QString destPath = "//MINERVA/3d5_2526/100_RESOURCES/Pipe/Pipeline_USD_2025-2026_src/resources/prism_title.png";

    if(FileHelper::FileExists(destPath)) {
        FileHelper::DeleteFile(destPath);
    }
    FileHelper::CopyFile(srcPath , destPath);

    return true;
}



int main(int argc, char *argv[])
{

    qDebug()<< "Maya path : " << SoftwareHelpers::getMayaPath();
    qDebug()<< "Maya preferences path : " << SoftwareHelpers::getMayaPrefsPath();

    qDebug()<< "Houdini path : " << SoftwareHelpers::getHoudiniPath();
    qDebug()<< "Houdini preferences path : " << SoftwareHelpers::getHoudiniPrefsPath();

    qDebug()<< "Zbrush path : " << SoftwareHelpers::getZbrushPath();
    qDebug()<< "Substance Painter path : " << SoftwareHelpers::getSubstancePainterPath();
    qDebug()<< "Substance Painter prefs path : " << SoftwareHelpers::getSubstancePrefsPath();

    qDebug()<< "Prism path : " << SoftwareHelpers::getPrismPath();
    qDebug()<< "Prism preferences path : " << SoftwareHelpers::getPrismPrefsPath();

    killApplication("Prism.exe");

    /// Get the name of the computer
    QString computerName = QSysInfo::machineHostName();
    if(computerName == "MTP3D558") {
        resetResourcePath();
    }


    QApplication a(argc, argv);
    MainWizard w;
    w.show();
    return a.exec();
}
