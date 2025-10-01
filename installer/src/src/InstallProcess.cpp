#include "InstallProcess.h"

InstallProcess::InstallProcess()
{

}

QStringList InstallProcess::arguments() const
{
    return m_arguments;
}

void InstallProcess::setArguments(const QStringList &newArguments)
{
    m_arguments = newArguments;
}

QStringList InstallProcess::selectedComponents() const
{
    return m_selectedComponents;
}

void InstallProcess::setSelectedComponents(const QStringList &newSelectedComponents)
{
    m_selectedComponents = newSelectedComponents;
}

void InstallProcess::log(const QString &message)
{
    emit(this->logMessage(message));
}

void InstallProcess::logError(const QString &message)
{
    emit(this->logMessage("<font color='red'>ERROR: </font>" + message ));
}

void InstallProcess::logSuccess(const QString &message)
{
    emit(this->logMessage("<font color='green'>SUCCESS: </font>" + message ));
}

void InstallProcess::run()
{
    emit installationStarted();
    
    bool success = install();
    
    if (success) {
        logSuccess("Installation completed successfully!");
    } else {
        logError("Installation failed!");
    }
    
    emit installationFinished();
}
