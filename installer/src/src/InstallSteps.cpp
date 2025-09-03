#include "InstallSteps.h"
#include <QDir>
#include <QFile>
#include <QThread>
#include <QStandardPaths>
#include <QSysInfo>
#include <QCoreApplication>


CheckSystemRequirementsStep::CheckSystemRequirementsStep(QObject *parent)
    :InstallStep("Check system requirement",parent)
{

}

InstallStep::StepResult CheckSystemRequirementsStep::execute()
{

    QThread::sleep(1); // Simulate some work being done
    return Success;
}

InstallMainPrismPluggin::InstallMainPrismPluggin(QObject *parent)
    :InstallStep("Install the main prism plugin",parent)
{

}

InstallStep::StepResult InstallMainPrismPluggin::execute()
{

    QThread::sleep(1); // Simulate some work being done
    return Success;
}

InstallZbrushPrismPluggin::InstallZbrushPrismPluggin(QObject *parent)
    :InstallStep("Install the zbrush plugin",parent)
{

}

InstallStep::StepResult InstallZbrushPrismPluggin::execute()
{

    QThread::sleep(1); // Simulate some work being done
    return Success;
}

InstallSubstancePainterPluggin::InstallSubstancePainterPluggin(QObject *parent)
    :InstallStep("Install the substance painter plugin" , parent)
{

}

InstallStep::StepResult InstallSubstancePainterPluggin::execute()
{

    QThread::sleep(1); // Simulate some work being done
    return Success;
}

InstallMayaSaveAsScript::InstallMayaSaveAsScript(QObject *parent)
    :InstallStep("Install the maya save as script",parent)
{

}

InstallStep::StepResult InstallMayaSaveAsScript::execute()
{

    QThread::sleep(1); // Simulate some work being done
    return Success;
}

InstallMayaShelf::InstallMayaShelf(QObject *parent)
:InstallStep("Install the maya shelf", parent)
{

}

InstallStep::StepResult InstallMayaShelf::execute()
{

    QThread::sleep(1); // Simulate some work being done
    return Success;
}
