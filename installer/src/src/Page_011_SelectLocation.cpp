#include "Page_011_SelectLocation.h"
#include "ui_Page_011_SelectLocation.h"

#include <QFileDialog>
#include <QDir>
#include <QAction>
#include <QDebug>

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

