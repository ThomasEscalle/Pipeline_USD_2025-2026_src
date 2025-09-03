#ifndef PAGE__12_INSTALATION_H
#define PAGE__12_INSTALATION_H

#include <QWizardPage>

class InstallProcess;

namespace Ui {
class Page_012_Instalation;
}

class Page_012_Instalation : public QWizardPage
{
    Q_OBJECT

public:
    Page_012_Instalation();
    ~Page_012_Instalation();

    // Quand la page est focus
    void initializePage() override;

    // Lance l'installation
    void startInstallation();

    void log(const QString& message);


    // Recupere l'id de la page qui viens apres celle la
    int nextId() const override;

    // Getter pour voir si la page est prete a passer a la suivante
    bool isComplete() const override { return m_isComplete;}

    // Setter pour mettre la page en temps que complete
    void setComplete(const bool& isComplete) {m_isComplete = isComplete; emit completeChanged();}

private slots:
    void onLogMessage(const QString &message);
    void onInstallationFinished();

private:
    bool m_isComplete = false;
    Ui::Page_012_Instalation *ui;
    InstallProcess *m_installProcess;
};

#endif // PAGE__12_INSTALATION_H
