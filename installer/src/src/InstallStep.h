#ifndef INSTALLSTEP_H
#define INSTALLSTEP_H

#include <QString>
#include <QObject>

class InstallStep : public QObject
{
    Q_OBJECT

public:
    enum StepResult {
        Success,
        Failed,
        Cancelled
    };

    explicit InstallStep(const QString &description, QObject *parent = nullptr);
    virtual ~InstallStep();

    // Méthode virtuelle pure que chaque étape doit implémenter
    virtual StepResult execute() = 0;

    // Getters
    QString description() const { return m_description; }
    bool isCompleted() const { return m_completed; }
    StepResult result() const { return m_result; }
    QString errorMessage() const { return m_errorMessage; }

signals:
    void stepProgress(const QString &message);
    void stepCompleted(InstallStep::StepResult result);

protected:
    void setCompleted(StepResult result, const QString &errorMessage = QString());
    void emitProgress(const QString &message);

private:
    QString m_description;
    bool m_completed;
    StepResult m_result;
    QString m_errorMessage;
};

#endif // INSTALLSTEP_H
