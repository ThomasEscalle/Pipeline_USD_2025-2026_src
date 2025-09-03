#include "src/Page_000_Welcome.h"

#include "src/MainWizard.h"
#include "ui_Page_000_Welcome.h"

Page_000_Welcome::Page_000_Welcome() {
    setTitle("Welcome");
    setSubTitle("Select what you want to do.");

    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));

    ui = new Ui::Page_000_Welcome();
    ui->setupUi(this);
}

int Page_000_Welcome::nextId() const {
    if(ui->rb_InstallTools->isChecked()) {
        return MainWizard::PAGE_010_SELECTCOMPONENTS;
    }
    else {
        return MainWizard::PAGE_020_NAMEANDLOCATION;
    }
}
