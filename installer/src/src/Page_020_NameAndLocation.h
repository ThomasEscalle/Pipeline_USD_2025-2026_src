#ifndef PAGE__2__NAMEANDLOCATION_H
#define PAGE__2__NAMEANDLOCATION_H

#include <QWizardPage>

namespace Ui {
class Page_020_NameAndLocation;
}

class Page_020_NameAndLocation : public QWizardPage
{
    Q_OBJECT

public:
    Page_020_NameAndLocation();
    ~Page_020_NameAndLocation();

    int nextId() const override;

private slots:
    void on_btn_select_clicked();

private:
    Ui::Page_020_NameAndLocation *ui;
};

#endif // PAGE__2__NAMEANDLOCATION_H
