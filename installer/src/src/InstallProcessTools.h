#ifndef INSTALLPROCESSTOOLS_H
#define INSTALLPROCESSTOOLS_H

#include "InstallProcess.h"

class InstallProcessTools : public InstallProcess
{
    Q_OBJECT

public:
    explicit InstallProcessTools(QObject *parent = nullptr);
    virtual ~InstallProcessTools();
    
    // Méthode pour définir les composants sélectionnés
    void setSelectedComponents(const QStringList& selectedComponents);

protected:
    // Implémentation de la méthode virtuelle pure
    virtual void createInstallationSteps() override;

private:
    QStringList m_selectedComponents;
};

#endif // INSTALLPROCESSTOOLS_H
