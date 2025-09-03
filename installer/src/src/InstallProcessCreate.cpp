#include "InstallProcessCreate.h"
#include "InstallStep.h"
#include "InstallSteps.h"
#include <QStandardPaths>

InstallProcessCreate::InstallProcessCreate(QObject *parent)
    : InstallProcess(parent)
{
}

InstallProcessCreate::~InstallProcessCreate()
{
}

void InstallProcessCreate::createInstallationSteps()
{
    // Réinitialiser les compteurs
    m_totalSteps = 0;

    // Étape 1: Validation des paramètres de création
    addInstallStep(new CheckSystemRequirementsStep(this));
    addInstallStep(new InstallMainPrismPluggin(this));
    addInstallStep(new InstallZbrushPrismPluggin(this));
    addInstallStep(new InstallSubstancePainterPluggin(this));
    addInstallStep(new InstallMayaSaveAsScript(this));
    addInstallStep(new InstallMayaShelf(this));
}
