#include "Page_020_NameAndLocation.h"
#include "ui_Page_020_NameAndLocation.h"

#include <QFileDialog>
#include <QDir>

#include "MainWizard.h"

Page_020_NameAndLocation::Page_020_NameAndLocation()
    : QWizardPage()
    , ui(new Ui::Page_020_NameAndLocation)
{
    ui->setupUi(this);

    // Set the title and subtitle
    setTitle(tr("Name and Location"));
    setSubTitle(tr("Please enter the name and location for the new project."));
    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));

    ui->le_path->setText(QDir::homePath());
}

Page_020_NameAndLocation::~Page_020_NameAndLocation()
{
    delete ui;
}


int Page_020_NameAndLocation::nextId() const
{
    return MainWizard::PAGE_021_OPTIONS;
}

void Page_020_NameAndLocation::on_btn_select_clicked()
{
    /// If the line edit is empty, start at the home directory
    QString path = ui->le_path->text();
    if (path.isEmpty()) {
        path = QDir::homePath();
    }

    QString dir = QFileDialog::getExistingDirectory(this, tr("Select Installation Directory"), path);
    if (!dir.isEmpty()) {
        ui->le_path->setText(dir);
    }
}

