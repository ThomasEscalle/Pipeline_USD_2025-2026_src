#include "Page_023_Conclusion.h"
#include "ui_Page_023_Conclusion.h"

#include "MainWizard.h"

#include "Page_022_Creation.h"

#include <QDesktopServices>
#include <QUrl>

Page_023_Conclusion::Page_023_Conclusion()
    : QWizardPage()
    , ui(new Ui::Page_023_Conclusion)
{
    ui->setupUi(this);

    // title and subtitle
    setTitle(tr("Conclusion"));
    setSubTitle(tr("The creation of the project is now complete."));
    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));

    setFinalPage(true);


}

Page_023_Conclusion::~Page_023_Conclusion()
{
    delete ui;
}

int Page_023_Conclusion::nextId() const
{
    return -1;
}

void Page_023_Conclusion::on_btn_whatsnext_clicked()
{
    /// Open the url of the documentation
    /// https://thomasescalle.github.io/Pipeline_USD_2025/demarage/

    QDesktopServices::openUrl(QUrl("https://thomasescalle.github.io/Pipeline_USD_2025/demarage/"));
}


void Page_023_Conclusion::on_btn_explorer_clicked()
{
    // Récupérer les composants sélectionnés depuis la page de sélection
    MainWizard* mainWizard = qobject_cast<MainWizard*>(wizard());
    if (mainWizard) {
        Page_022_Creation* selectPage = qobject_cast<Page_022_Creation*>(
            mainWizard->page(MainWizard::PAGE_022_CREATION));
        if (selectPage) {
            QDesktopServices::openUrl(QUrl(selectPage->createdPath()));
        }
    }

}

