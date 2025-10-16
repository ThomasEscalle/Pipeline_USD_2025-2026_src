#ifndef PAGE__11_SELECTLOCATION_H
#define PAGE__11_SELECTLOCATION_H

#include <QWizardPage>

namespace Ui {
class Page_011_SelectLocation;
}

class Page_011_SelectLocation : public QWizardPage
{
    Q_OBJECT

public:
    explicit Page_011_SelectLocation();
    ~Page_011_SelectLocation();


    int nextId() const override;



    QString getUsername() const;
    QString getAbbreviation() const;
    QString getArPath() const;

    void saveUserData();
    void loadUserData();
    void searchForARPath();

private slots:
    void on_btn_selectLocation_clicked();
    void autofillFields();
    void on_btn_BrowseAR_clicked();

private:
    Ui::Page_011_SelectLocation *ui;
};

#endif // PAGE__11_SELECTLOCATION_H
