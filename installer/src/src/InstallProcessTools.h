#ifndef INSTALLPROCESSTOOLS_H
#define INSTALLPROCESSTOOLS_H

#include "InstallProcess.h"

class InstallProcessTools : public InstallProcess
{
    Q_OBJECT

public:
    explicit InstallProcessTools(QObject *parent = nullptr);
    virtual ~InstallProcessTools();

public:
    bool install() override;
};

#endif // INSTALLPROCESSTOOLS_H
