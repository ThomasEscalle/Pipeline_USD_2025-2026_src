#include "Page_012_Instalation.h"
#include "ui_Page_012_Instalation.h"
#include "InstallProcessTools.h"
#include <QApplication>
#include "MainWizard.h"
#include "Page_010_SelectComponents.h"

Page_012_Instalation::Page_012_Instalation()
    : QWizardPage()
    , ui(new Ui::Page_012_Instalation)
    , m_installProcess(new InstallProcessTools(this))
{
    ui->setupUi(this);

    // Title and subtitle
    setTitle(tr("Installation"));
    setSubTitle(tr("Please wait while the tools are being installed..."));
    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));

    // Connecter les signaux de InstallProcess
    connect(m_installProcess, &InstallProcess::logMessage, 
            this, &Page_012_Instalation::onLogMessage);
    connect(m_installProcess, &InstallProcess::installationFinished, 
            this, &Page_012_Instalation::onInstallationFinished);


}

Page_012_Instalation::~Page_012_Instalation()
{
    delete ui;
}

void Page_012_Instalation::initializePage()
{
    // Récupérer les composants sélectionnés depuis la page de sélection
    MainWizard* mainWizard = qobject_cast<MainWizard*>(wizard());
    if (mainWizard) {
        Page_010_SelectComponents* selectPage = qobject_cast<Page_010_SelectComponents*>(
            mainWizard->page(MainWizard::PAGE_010_SELECTCOMPONENTS));
        if (selectPage) {
            QStringList selectedComponents = selectPage->getSelectedComponents();
            m_installProcess->setSelectedComponents(selectedComponents);
        }
    }
    
    // Démarrer l'installation
    startInstallation();
}

void Page_012_Instalation::startInstallation()
{
    // Démarrer le processus d'installation
    m_installProcess->install();
}

void Page_012_Instalation::log(const QString &message)
{
    ui->textEdit->append(message);
}

int Page_012_Instalation::nextId() const
{
    return MainWizard::PAGE_013_CONCLUSION;
}

void Page_012_Instalation::onLogMessage(const QString &message)
{
    log(message);
}

void Page_012_Instalation::onInstallationFinished()
{
    setComplete(true);
}
