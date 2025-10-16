#include "Page_011_SelectLocation.h"
#include "ui_Page_011_SelectLocation.h"

#include <QFileDialog>
#include <QDir>
#include <QAction>
#include <QDebug>
#include <QSettings>
#include <QStandardPaths>
#include <QMessageBox>

#include "MainWizard.h"

Page_011_SelectLocation::Page_011_SelectLocation()
    : QWizardPage()
    , ui(new Ui::Page_011_SelectLocation)
{
    ui->setupUi(this);


    // Title and subtitle
    setTitle(tr("Options"));
    setSubTitle(tr("Please select the desired options for the installation."));
    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));

    // Add a "Autofill action" to autofill the fields
    QAction *autofillAction = new QAction(tr("Autofill"), this);
    autofillAction->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_A));
    connect(autofillAction, &QAction::triggered, this, &Page_011_SelectLocation::autofillFields);
    addAction(autofillAction);

    // Load saved user data
    loadUserData();
    
    // Search for AR path only if none was loaded from preferences
    if (ui->le_ArPath->text().isEmpty()) {
        searchForARPath();
    }

    setCommitPage(true);
}

Page_011_SelectLocation::~Page_011_SelectLocation()
{
    delete ui;
}

void Page_011_SelectLocation::autofillFields()
{
    qDebug()<<"Autofill";
    // Example autofill logic
    ui->le_username->setText("Thomas");
    ui->le_abreviation->setText("Tho");
}

int Page_011_SelectLocation::nextId() const
{
    // Save user data before proceeding to next page
    const_cast<Page_011_SelectLocation*>(this)->saveUserData();
    return MainWizard::PAGE_012_INSTALATION;
}

void Page_011_SelectLocation::saveUserData()
{
    QString appDataPath = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
    QDir().mkpath(appDataPath); // Create directory if it doesn't exist
    
    QSettings settings(appDataPath + "/user_preferences.ini", QSettings::IniFormat);
    settings.setValue("user/username", ui->le_username->text());
    settings.setValue("user/abbreviation", ui->le_abreviation->text());
    settings.setValue("user/arPath", ui->le_ArPath->text());
    settings.sync();
    
    qDebug() << "User data saved to:" << appDataPath + "/user_preferences.ini";
}

void Page_011_SelectLocation::loadUserData()
{
    QString appDataPath = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
    QSettings settings(appDataPath + "/user_preferences.ini", QSettings::IniFormat);
    
    QString savedUsername = settings.value("user/username", "").toString();
    QString savedAbbreviation = settings.value("user/abbreviation", "").toString();
    QString savedArPath = settings.value("user/arPath", "").toString();
    
    if (!savedUsername.isEmpty()) {
        ui->le_username->setText(savedUsername);
        qDebug() << "Loaded username:" << savedUsername;
    }
    
    if (!savedAbbreviation.isEmpty()) {
        ui->le_abreviation->setText(savedAbbreviation);
        qDebug() << "Loaded abbreviation:" << savedAbbreviation;
    }
    
    if (!savedArPath.isEmpty()) {
        ui->le_ArPath->setText(savedArPath);
        qDebug() << "Loaded AR path:" << savedArPath;
    }
}

void Page_011_SelectLocation::searchForARPath()
{
    QStringList possiblePaths = {

    };

    for(auto it: possiblePaths) {
        QDir assetResolverDir(it);
        if (assetResolverDir.exists("maya") && assetResolverDir.exists("hou")) {
            ui->le_ArPath->setText(it);
            qDebug() << "Found valid Asset Resolver path:" << it;
            return;
        }
    }
}


void Page_011_SelectLocation::on_btn_selectLocation_clicked()
{


}

QString Page_011_SelectLocation::getArPath() const
{
    return ui->le_ArPath->text();
}

QString Page_011_SelectLocation::getUsername() const
{
    return ui->le_username->text();
}

QString Page_011_SelectLocation::getAbbreviation() const
{
    return ui->le_abreviation->text();
}


void Page_011_SelectLocation::on_btn_BrowseAR_clicked()
{
    QString dir = QFileDialog::getExistingDirectory(this, tr("Select Asset Resolver Path"), QDir::homePath());
    if (!dir.isEmpty()) {
        /// Check if the given directory contains a "maya" and a "hou" subfolder, 
        QDir assetResolverDir(dir);
        if (assetResolverDir.exists("maya") && assetResolverDir.exists("hou")) {
            ui->le_ArPath->setText(dir);
        } else {
            QMessageBox::warning(this, tr("Invalid Directory"), tr("The selected directory must contain 'maya' and 'hou' subfolders."));
        }
    }
}

