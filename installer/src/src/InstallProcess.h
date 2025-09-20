#ifndef INSTALLPROCESS_H
#define INSTALLPROCESS_H

#include <QStringList>
#include <QCoreApplication>
#include <QObject>

class InstallProcess : public QObject
{
    Q_OBJECT

public:

    InstallProcess();

    virtual bool install() = 0;


    QStringList arguments() const;
    void setArguments(const QStringList &newArguments);

    QStringList selectedComponents() const;
    void setSelectedComponents(const QStringList &newSelectedComponents);


    void log(const QString& message);
    void logError(const QString& message);
    void logSuccess(const QString& message);

    void processEvents() { QCoreApplication::processEvents(); }

signals:
    void logMessage(const QString& message);
    void installationFinished();

private:
    QStringList m_arguments;
    QStringList m_selectedComponents;
};

#endif // INSTALLPROCESS_H
