#include "src/MainWizard.h"

#include <QApplication>

#include "SoftwareHelpers.h"
#include <QDebug>

int main(int argc, char *argv[])
{

    qDebug()<< "Maya path : " << SoftwareHelpers::getMayaPath();
    qDebug()<< "Maya preferences path : " << SoftwareHelpers::getMayaPrefsPath();

    qDebug()<< "Houdini path : " << SoftwareHelpers::getHoudiniPath();
    qDebug()<< "Houdini preferences path : " << SoftwareHelpers::getHoudiniPrefsPath();

    qDebug()<< "Zbrush path : " << SoftwareHelpers::getZbrushPath();
    qDebug()<< "Substance Painter path : " << SoftwareHelpers::getSubstancePainterPath();

    QApplication a(argc, argv);
    MainWizard w;
    w.show();
    return a.exec();
}
