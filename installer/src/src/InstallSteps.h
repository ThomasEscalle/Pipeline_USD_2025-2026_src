#ifndef INSTALLSTEPS_H
#define INSTALLSTEPS_H

#include "InstallStep.h"
#include <QDir>
#include <QThread>


// Étape pour vérifier les prérequis système
class CheckSystemRequirementsStep : public InstallStep
{
    Q_OBJECT
public:
    explicit CheckSystemRequirementsStep(QObject *parent = nullptr);
    StepResult execute() override;
};

/// Installe le pluggin principal de prism
class InstallMainPrismPluggin : public InstallStep
{
    Q_OBJECT
public:
    explicit InstallMainPrismPluggin(QObject *parent = nullptr);
    StepResult execute() override;
};

/// Installe le pluggin zbrush de prism
class InstallZbrushPrismPluggin : public InstallStep
{
    Q_OBJECT
public:
    explicit InstallZbrushPrismPluggin(QObject *parent = nullptr);
    StepResult execute() override;
};

/// Installe le pluggin substance painter de prism
class InstallSubstancePainterPluggin : public InstallStep
{
    Q_OBJECT
public:
    explicit InstallSubstancePainterPluggin(QObject *parent = nullptr);
    StepResult execute() override;
};

// Installe le script maya 
class InstallMayaSaveAsScript : public InstallStep
{
    Q_OBJECT
public:
    explicit InstallMayaSaveAsScript(QObject *parent = nullptr);
    StepResult execute() override;
};

// Installe le shelf maya
class InstallMayaShelf : public InstallStep
{
    Q_OBJECT
public:
    explicit InstallMayaShelf(QObject *parent = nullptr);
    StepResult execute() override;
};

#endif // INSTALLSTEPS_H
