#ifndef INSTALLPROCESS_H
#define INSTALLPROCESS_H

#include <QProcess>
#include <QTimer>
#include <QString>
#include <QQueue>

class InstallStep;

class InstallProcess : public QProcess
{
    Q_OBJECT

public:
    explicit InstallProcess(QObject *parent = nullptr);
    virtual ~InstallProcess();

    void startInstallation();
    
    int totalSteps() const { return m_totalSteps; }
    int completedSteps() const { return m_completedSteps; }

signals:
    void logMessage(const QString &message);
    void installationFinished();
    void installationProgress(int completed, int total);

protected:
    // Méthode virtuelle pure que les sous-classes doivent implémenter
    virtual void createInstallationSteps() = 0;
    
    // Méthodes utilitaires pour les sous-classes
    void addInstallStep(InstallStep *step);
    void cleanupSteps();

private slots:
    void processNextStep();
    void onStepProgress(const QString &message);
    void onStepCompleted(int result);

protected:
    QTimer *m_timer;
    QQueue<InstallStep*> m_installSteps;
    InstallStep *m_currentStep;
    int m_totalSteps;
    int m_completedSteps;
};

#endif // INSTALLPROCESS_H
