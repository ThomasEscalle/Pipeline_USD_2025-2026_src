#include "InstallProcessTools.h"
#include <QStandardPaths>

InstallProcessTools::InstallProcessTools(QObject *parent)
{
}

InstallProcessTools::~InstallProcessTools()
{
}

bool InstallProcessTools::install()
{

    log("Hey");
    emit this->installationFinished();
    return true;
}

