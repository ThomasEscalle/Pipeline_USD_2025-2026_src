#include "Page_013_Conclusion.h"
#include "ui_Page_013_Conclusion.h"

#include <QDesktopServices>
#include <QUrl>

Page_013_Conclusion::Page_013_Conclusion()
    : QWizardPage()
    , ui(new Ui::Page_013_Conclusion)
{
    ui->setupUi(this);

    // Title and subtitle
    setTitle(tr("Installation complete"));
    setSubTitle(tr("The installation is complete. Click Finish to exit the installer."));
    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));

    setFinalPage(true);
}

Page_013_Conclusion::~Page_013_Conclusion()
{
    delete ui;
}

int Page_013_Conclusion::nextId() const
{
    return -1;
}

void Page_013_Conclusion::on_btn_WhatsNext_clicked()
{
    /// Open the url of the documentation
    /// https://thomasescalle.github.io/Pipeline_USD_2025/demarage/

    QDesktopServices::openUrl(QUrl("https://thomasescalle.github.io/Pipeline_USD_2025/demarage/"));
}

