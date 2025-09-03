#ifndef PAGE__22_CREATION_H
#define PAGE__22_CREATION_H

#include <QWizardPage>

class InstallProcess;

namespace Ui {
class Page_022_Creation;
}

class Page_022_Creation : public QWizardPage
{
    Q_OBJECT

public:
    Page_022_Creation();
    ~Page_022_Creation();

    // Quand la page est focus
    void initializePage() override;

    // Lance la création
    void startCreation();

    void log(const QString& message);

    // Recupere l'id de la page qui viens apres celle la
    int nextId() const override;

    // Getter pour voir si la page est prete a passer a la suivante
    bool isComplete() const override { return m_isComplete;}

    // Setter pour mettre la page en temps que complete
    void setComplete(const bool& isComplete) {m_isComplete = isComplete; emit completeChanged();}

private slots:
    void onLogMessage(const QString &message);
    void onCreationFinished();

private:
    bool m_isComplete = false;
    Ui::Page_022_Creation* ui;
    InstallProcess *m_createProcess;
};

#endif // PAGE__22_CREATION_H
