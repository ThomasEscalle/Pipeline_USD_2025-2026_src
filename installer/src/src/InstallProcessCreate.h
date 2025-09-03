#ifndef INSTALLPROCESSCREATE_H
#define INSTALLPROCESSCREATE_H

#include "InstallProcess.h"

class InstallProcessCreate : public InstallProcess
{
    Q_OBJECT

public:
    explicit InstallProcessCreate(QObject *parent = nullptr);
    virtual ~InstallProcessCreate();

protected:
    // Implémentation de la méthode virtuelle pure
    virtual void createInstallationSteps() override;
};

#endif // INSTALLPROCESSCREATE_H
