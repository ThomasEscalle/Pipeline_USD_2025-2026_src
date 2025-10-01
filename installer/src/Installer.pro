QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    src/FileHelper.cpp \
    src/InstallProcess.cpp \
    src/InstallProcessTools.cpp \
    src/InstallProcessCreate.cpp \
    src/Page_010_SelectComponents.cpp \
    src/Page_011_SelectLocation.cpp \
    src/Page_012_Instalation.cpp \
    src/Page_013_Conclusion.cpp \
    src/Page_020_NameAndLocation.cpp \
    src/Page_021_Options.cpp \
    src/Page_022_Creation.cpp \
    src/Page_023_Conclusion.cpp \
    src/SoftwareHelpers.cpp \
    src/main.cpp \
    src/MainWizard.cpp \
    src/Page_000_Welcome.cpp

HEADERS += \
    src/FileHelper.h \
    src/InstallProcess.h \
    src/InstallProcessTools.h \
    src/InstallProcessCreate.h \
    src/Page_010_SelectComponents.h \
    src/MainWizard.h \
    src/Page_000_Welcome.h \
    src/Page_011_SelectLocation.h \
    src/Page_012_Instalation.h \
    src/Page_013_Conclusion.h \
    src/Page_020_NameAndLocation.h \
    src/Page_021_Options.h \
    src/Page_022_Creation.h \
    src/Page_023_Conclusion.h \
    src/SoftwareHelpers.h

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RC_ICONS = rc/appico.ico

FORMS += \
    ui/Page_022_Creation.ui \
    ui/Page_023_Conclusion.ui \
    ui/Page_021_Options.ui \
    ui/Page_013_Conclusion.ui \
    ui/Page_012_Instalation.ui \
    ui/Page_011_SelectLocation.ui \
    ui/Page_020_NameAndLocation.ui \
    ui/Page_010_SelectComponents.ui \
    ui/Page_000_Welcome.ui

RESOURCES += \
    rc/rc.qrc
