#include "Page_011_SelectLocation.h"
#include "ui_Page_011_SelectLocation.h"

#include <QFileDialog>
#include <QDir>

#include "MainWizard.h"

Page_011_SelectLocation::Page_011_SelectLocation()
    : QWizardPage()
    , ui(new Ui::Page_011_SelectLocation)
{
    ui->setupUi(this);

    ui->le_location->setText(QDir::homePath());

    // Title and subtitle
    setTitle(tr("Select Installation Location"));
    setSubTitle(tr("Select the location where you want to install the application."));
    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));

    setCommitPage(true);
}

Page_011_SelectLocation::~Page_011_SelectLocation()
{
    delete ui;
}

int Page_011_SelectLocation::nextId() const
{
    return MainWizard::PAGE_012_INSTALATION;
}

void Page_011_SelectLocation::on_btn_selectLocation_clicked()
{
    /// If the line edit is empty, start at the home directory
    QString path = ui->le_location->text();
    if (path.isEmpty()) {
        path = QDir::homePath();
    }

    QString dir = QFileDialog::getExistingDirectory(this, tr("Select Installation Directory"), path);
    if (!dir.isEmpty()) {
        ui->le_location->setText(dir);
    }

}

