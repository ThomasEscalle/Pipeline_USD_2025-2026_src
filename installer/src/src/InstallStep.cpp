#include "InstallStep.h"

InstallStep::InstallStep(const QString &description, QObject *parent)
    : QObject(parent)
    , m_description(description)
    , m_completed(false)
    , m_result(Success)
{
}

InstallStep::~InstallStep()
{
}

void InstallStep::setCompleted(StepResult result, const QString &errorMessage)
{
    m_completed = true;
    m_result = result;
    m_errorMessage = errorMessage;
    emit stepCompleted(result);
}

void InstallStep::emitProgress(const QString &message)
{
    emit stepProgress(message);
}
