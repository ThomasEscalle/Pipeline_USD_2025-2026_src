#ifndef PAGE__13_CONCLUSION_H
#define PAGE__13_CONCLUSION_H

#include <QWizardPage>

namespace Ui {
class Page_013_Conclusion;
}

class Page_013_Conclusion : public QWizardPage
{
    Q_OBJECT

public:
    explicit Page_013_Conclusion();
    ~Page_013_Conclusion();

    int nextId() const override;

private slots:
    void on_btn_WhatsNext_clicked();

private:
    Ui::Page_013_Conclusion *ui;
};

#endif // PAGE__13_CONCLUSION_H
