#ifndef SOFTWAREHELPERS_H
#define SOFTWAREHELPERS_H

#include <QObject>

class SoftwareHelpers : public QObject
{
    Q_OBJECT
public:
    /// Return the path of maya
    static QString getMayaPath();
    static QString getMayaPrefsPath();

    static QString getHoudiniPath();
    static QString getHoudiniPrefsPath();

    static QString getZbrushPath();

    static QString getSubstancePainterPath();

    static QString getPrismPath();
};


#endif // SOFTWAREHELPERS_H
