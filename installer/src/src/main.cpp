#include "src/MainWizard.h"

#include <QApplication>

#include "SoftwareHelpers.h"
#include <QDebug>


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





int main(int argc, char *argv[])
{

    qDebug()<< "Maya path : " << SoftwareHelpers::getMayaPath();
    qDebug()<< "Maya preferences path : " << SoftwareHelpers::getMayaPrefsPath();

    qDebug()<< "Houdini path : " << SoftwareHelpers::getHoudiniPath();
    qDebug()<< "Houdini preferences path : " << SoftwareHelpers::getHoudiniPrefsPath();

    qDebug()<< "Zbrush path : " << SoftwareHelpers::getZbrushPath();
    qDebug()<< "Substance Painter path : " << SoftwareHelpers::getSubstancePainterPath();
    
    qDebug()<< "Prism path : " << SoftwareHelpers::getPrismPath();
    qDebug()<< "Prism preferences path : " << SoftwareHelpers::getPrismPrefsPath();

    killApplication("Prism.exe");

    QApplication a(argc, argv);
    MainWizard w;
    w.show();
    return a.exec();
}
