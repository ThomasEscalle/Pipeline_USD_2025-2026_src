#include "Page_012_Instalation.h"
#include "ui_Page_012_Instalation.h"
#include "InstallProcessTools.h"
#include <QApplication>
#include "MainWizard.h"
#include "Page_010_SelectComponents.h"
#include "Page_011_SelectLocation.h"

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
            this, &Page_012_Instalation::onLogMessage, Qt::QueuedConnection);
    connect(m_installProcess, &InstallProcess::installationFinished, 
            this, &Page_012_Instalation::onInstallationFinished, Qt::QueuedConnection);
    connect(m_installProcess, &InstallProcess::installationStarted,
            this, [this](){ log("Starting installation..."); }, Qt::QueuedConnection);


}

Page_012_Instalation::~Page_012_Instalation()
{
    if (m_installProcess && m_installProcess->isRunning()) {
        m_installProcess->quit();
        m_installProcess->wait();
    }
    delete ui;
}

void Page_012_Instalation::initializePage()
{
    MainWizard* mainWizard = qobject_cast<MainWizard*>(wizard());
    if (mainWizard) {
        // Récupérer les composants sélectionnés depuis la page de sélection
        Page_010_SelectComponents* selectPage = qobject_cast<Page_010_SelectComponents*>(
            mainWizard->page(MainWizard::PAGE_010_SELECTCOMPONENTS));
        if (selectPage) {
            QStringList selectedComponents = selectPage->getSelectedComponents();
            m_installProcess->setSelectedComponents(selectedComponents);
        }

        /// Recupere les username et abreviation de la page "011_Select_location
        Page_011_SelectLocation* locationPage = qobject_cast<Page_011_SelectLocation*>(
            mainWizard->page(MainWizard::PAGE_011_SELECTLOCATION));
        if (locationPage) {

            InstallProcessTools* install_tools = dynamic_cast<InstallProcessTools*>(m_installProcess);
            QString username = locationPage->getUsername();
            QString abbreviation = locationPage->getAbbreviation();
            QString arPath = locationPage->getArPath();
            install_tools->setUsername(username);
            install_tools->setAbreviation(abbreviation);
            install_tools->setArPath(arPath);
        }
    }
    
    



    // Démarrer l'installation
    startInstallation();
}

void Page_012_Instalation::startInstallation()
{
    // Démarrer le thread d'installation
    if (!m_installProcess->isRunning()) {
        m_installProcess->start();
    }
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
