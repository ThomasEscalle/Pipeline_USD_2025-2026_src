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


    // Title and subtitle
    setTitle(tr("Options"));
    setSubTitle(tr("Please select the desired options for the installation."));
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


}

QString Page_011_SelectLocation::getUsername() const
{
    return ui->le_username->text();
}

QString Page_011_SelectLocation::getAbbreviation() const
{
    return ui->le_abreviation->text();
}

