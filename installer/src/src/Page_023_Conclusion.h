#ifndef PAGE__23_CONCLUSION_H
#define PAGE__23_CONCLUSION_H

#include <QWizardPage>

namespace Ui {
class Page_023_Conclusion;
}

class Page_023_Conclusion : public QWizardPage
{
    Q_OBJECT

public:
    explicit Page_023_Conclusion();
    ~Page_023_Conclusion();

    int nextId() const override;

private slots:
    void on_btn_whatsnext_clicked();
    void on_btn_explorer_clicked();

private:
    Ui::Page_023_Conclusion *ui;
};

#endif // PAGE__23_CONCLUSION_H
