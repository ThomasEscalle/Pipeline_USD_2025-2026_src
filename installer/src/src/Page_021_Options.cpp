#include "Page_021_Options.h"
#include "ui_Page_021_Options.h"

#include "MainWizard.h"

Page_021_Options::Page_021_Options()
    : QWizardPage()
    , ui(new Ui::Page_021_Options)
{
    ui->setupUi(this);

    // Set the title and subtitle
    setTitle(tr("Project options"));
    setSubTitle(tr("Please select the desired options for the new project."));
    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));
    setCommitPage(true);
}

Page_021_Options::~Page_021_Options()
{
    delete ui;
}

int Page_021_Options::nextId() const
{
    return MainWizard::PAGE_022_CREATION;
}
