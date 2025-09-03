#ifndef PAGE__WELCOME_H
#define PAGE__WELCOME_H

#include <QObject>
#include <QWizardPage>

// Forward declarations
namespace Ui {
    class Page_000_Welcome;
}

/// @brief Welcome page of the wizard
/// This page allows the user to choose what they want to do.
class Page_000_Welcome : public QWizardPage
{
    Q_OBJECT
public:
    Page_000_Welcome();

    int nextId() const override;

private:
    // Ui form
    Ui::Page_000_Welcome *ui;

};


#endif // PAGE__WELCOME_H
