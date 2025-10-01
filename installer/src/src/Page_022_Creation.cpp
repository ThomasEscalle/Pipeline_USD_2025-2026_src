#include "Page_022_Creation.h"
#include "ui_Page_022_Creation.h"
#include "InstallProcessCreate.h"

#include "Page_020_NameAndLocation.h"

#include "FileHelper.h"
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
            this, &Page_022_Creation::onLogMessage, Qt::QueuedConnection);
    connect(m_createProcess, &InstallProcess::installationFinished, 
            this, &Page_022_Creation::onCreationFinished, Qt::QueuedConnection);
    connect(m_createProcess, &InstallProcess::installationStarted,
            this, [this](){ log("Starting project creation..."); }, Qt::QueuedConnection);

}

Page_022_Creation::~Page_022_Creation()
{
    if (m_createProcess && m_createProcess->isRunning()) {
        m_createProcess->quit();
        m_createProcess->wait();
    }
    delete ui;
}

void Page_022_Creation::initializePage()
{
    // Récupérer les composants sélectionnés depuis la page de sélection
    MainWizard* mainWizard = qobject_cast<MainWizard*>(wizard());
    if (mainWizard) {
        Page_020_NameAndLocation* selectPage = qobject_cast<Page_020_NameAndLocation*>(
            mainWizard->page(MainWizard::PAGE_020_NAMEANDLOCATION));
        if (selectPage) {
            QString name = selectPage->getName();
            dynamic_cast<InstallProcessCreate*>(m_createProcess)->setProjectName(name);

            QString path = selectPage->getPath();
            dynamic_cast<InstallProcessCreate*>(m_createProcess)->setProjectPath(path);

            m_createdPath =FileHelper::JoinPath(path , name);
        }
    }



    // todo : Start the creation
    startCreation();


}

void Page_022_Creation::startCreation()
{
    // Démarrer le thread de création
    if (!m_createProcess->isRunning()) {
        m_createProcess->start();
    }
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

QString Page_022_Creation::createdPath() const
{
    return m_createdPath;
}
