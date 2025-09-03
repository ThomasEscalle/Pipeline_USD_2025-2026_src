#include "InstallProcess.h"
#include "InstallStep.h"
#include <QThread>
#include <QCoreApplication>

InstallProcess::InstallProcess(QObject *parent)
    : QProcess(parent)
    , m_timer(new QTimer(this))
    , m_currentStep(nullptr)
    , m_totalSteps(0)
    , m_completedSteps(0)
{
    // Connecter le timer au slot de traitement
    connect(m_timer, &QTimer::timeout, this, &InstallProcess::processNextStep);
    
    // Configurer le timer pour traiter une étape toutes les 100ms
    m_timer->setInterval(100);
    
    // Les étapes seront créées par les sous-classes
}

InstallProcess::~InstallProcess()
{
    if (m_timer->isActive()) {
        m_timer->stop();
    }
    cleanupSteps();
}

void InstallProcess::startInstallation()
{
    // Créer les étapes d'installation spécifiques à la sous-classe
    createInstallationSteps();
    
    m_completedSteps = 0;
    emit logMessage(tr("Starting installation process..."));
    emit installationProgress(0, m_totalSteps);
    m_timer->start();
}

void InstallProcess::addInstallStep(InstallStep *step)
{
    if (step) {
        m_installSteps.enqueue(step);
        m_totalSteps++;
        
        // Connecter les signaux de l'étape
        connect(step, &InstallStep::stepProgress, this, &InstallProcess::onStepProgress);
        connect(step, QOverload<InstallStep::StepResult>::of(&InstallStep::stepCompleted),
                this, QOverload<int>::of(&InstallProcess::onStepCompleted));
    }
}

void InstallProcess::processNextStep()
{
    // Si aucune étape en cours et qu'il y en a dans la queue
    if (!m_currentStep && !m_installSteps.isEmpty()) {
        m_currentStep = m_installSteps.dequeue();
        emit logMessage(QString("Starting: %1").arg(m_currentStep->description()));
        
        // Exécuter l'étape dans le thread actuel
        InstallStep::StepResult result = m_currentStep->execute();
        
        // Traiter le résultat immédiatement
        onStepCompleted(static_cast<int>(result));
    }
    // Si aucune étape en cours et la queue est vide
    else if (!m_currentStep && m_installSteps.isEmpty()) {
        // Installation terminée
        m_timer->stop();
        emit logMessage(tr("\nInstallation completed successfully!"));
        emit installationFinished();
    }
}

void InstallProcess::onStepProgress(const QString &message)
{
    emit logMessage(message);
}

void InstallProcess::onStepCompleted(int result)
{
    if (m_currentStep) {
        InstallStep::StepResult stepResult = static_cast<InstallStep::StepResult>(result);
        
        if (stepResult == InstallStep::Success) {
            m_completedSteps++;
            emit logMessage(QString("Completed: %1").arg(m_currentStep->description()));
            emit installationProgress(m_completedSteps, m_totalSteps);
        } else {
            // En cas d'erreur, arrêter l'installation
            m_timer->stop();
            emit logMessage(QString("Error in step: %1 - %2").arg(m_currentStep->description(), m_currentStep->errorMessage()));
            return;
        }
        
        // Nettoyer l'étape actuelle
        m_currentStep->deleteLater();
        m_currentStep = nullptr;
    }
}

void InstallProcess::cleanupSteps()
{
    // Nettoyer les étapes restantes
    while (!m_installSteps.isEmpty()) {
        InstallStep *step = m_installSteps.dequeue();
        step->deleteLater();
    }
    
    if (m_currentStep) {
        m_currentStep->deleteLater();
        m_currentStep = nullptr;
    }
}
