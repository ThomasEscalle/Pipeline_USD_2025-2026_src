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
    bool verify();


    bool install_MainPrismPlugin();
    bool install_SubstancePrismPlugin();
    bool install_ZBrushPrismPlugin();


    bool install_MayaSaveAs();
    bool install_MayaShelf();
    bool install_MayaAssetBrowser();
    bool install_MayaShotManager();

    bool install_HoudiniAssetBrowser();
    bool install_HoudiniCustomNodes();


    bool install_nameAndUsernamePrism();

    QString abreviation() const;
    void setAbreviation(const QString &newAbreviation);

    QString username() const;
    void setUsername(const QString &newUsername);


public:

    bool copyFolderRecursive(const QString &sourcePath, const QString &destPath);
    bool copyFile(const QString& sourcePath, const QString& destPath);
private:
    QString m_username;
    QString m_abreviation;
    QStringList m_successfulComponents;
    QStringList m_failedComponents;

};

#endif // INSTALLPROCESSTOOLS_H
