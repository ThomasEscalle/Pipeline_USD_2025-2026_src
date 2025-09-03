#include "Page_022_Creation.h"
#include "ui_Page_022_Creation.h"
#include "InstallProcessCreate.h"
#include <QApplication>
#include "MainWizard.h"


// Project creation in progress page
Page_022_Creation::Page_022_Creation()
    : QWizardPage()
    , ui(new Ui::Page_022_Creation)
    , m_createProcess(new InstallProcessCreate(this))
{
    ui->setupUi(this);

    // Title and subtitle
    setTitle(tr("Creating Project"));
    setSubTitle(tr("Please wait while the project is being created."));
    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));

    // Connecter les signaux de InstallProcessCreate
    connect(m_createProcess, &InstallProcess::logMessage, 
            this, &Page_022_Creation::onLogMessage);
    connect(m_createProcess, &InstallProcess::installationFinished, 
            this, &Page_022_Creation::onCreationFinished);

}

Page_022_Creation::~Page_022_Creation()
{
    delete ui;
}

void Page_022_Creation::initializePage()
{
    // todo : Start the creation
    startCreation();
}

void Page_022_Creation::startCreation()
{
    // Démarrer le processus de création
    m_createProcess->startInstallation();
}

void Page_022_Creation::log(const QString &message)
{
    ui->textEdit->append(message);
}

int Page_022_Creation::nextId() const
{
    return MainWizard::PAGE_023_CONCLUSION;
}

void Page_022_Creation::onLogMessage(const QString &message)
{
    log(message);
}

void Page_022_Creation::onCreationFinished()
{
    setComplete(true);
}
