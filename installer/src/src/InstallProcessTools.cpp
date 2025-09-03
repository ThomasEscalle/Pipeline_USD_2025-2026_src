#include "InstallProcessTools.h"
#include "InstallStep.h"
#include "InstallSteps.h"
#include <QStandardPaths>

InstallProcessTools::InstallProcessTools(QObject *parent)
    : InstallProcess(parent)
{
}

InstallProcessTools::~InstallProcessTools()
{
}

void InstallProcessTools::setSelectedComponents(const QStringList& selectedComponents)
{
    m_selectedComponents = selectedComponents;
}

void InstallProcessTools::createInstallationSteps()
{
    // Réinitialiser les compteurs
    m_totalSteps = 0;

    // Étape obligatoire: Validation des paramètres de création
    addInstallStep(new CheckSystemRequirementsStep(this));
    
    // Ajouter les étapes en fonction des composants sélectionnés
    if (m_selectedComponents.contains("Main prism plugin")) {
        addInstallStep(new InstallMainPrismPluggin(this));
    }
    
    if (m_selectedComponents.contains("Zbrush prim plugin")) {
        addInstallStep(new InstallZbrushPrismPluggin(this));
    }
    
    if (m_selectedComponents.contains("Substance painter plugin")) {
        addInstallStep(new InstallSubstancePainterPluggin(this));
    }
    
    if (m_selectedComponents.contains("Save as script")) {
        addInstallStep(new InstallMayaSaveAsScript(this));
    }
    
    if (m_selectedComponents.contains("Shelf")) {
        addInstallStep(new InstallMayaShelf(this));
    }
}
