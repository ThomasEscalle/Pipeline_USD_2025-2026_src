#ifndef PAGE__21_OPTIONS_H
#define PAGE__21_OPTIONS_H

#include <QWizardPage>

namespace Ui {
class Page_021_Options;
}

class Page_021_Options : public QWizardPage
{
    Q_OBJECT

public:
    explicit Page_021_Options();
    ~Page_021_Options();

    int nextId() const override;

private:
    Ui::Page_021_Options *ui;
};

#endif // PAGE__21_OPTIONS_H
