#ifndef MAINWIZARD_H
#define MAINWIZARD_H

#include <QWizard>

// Forward declarations
class Page_000_Welcome;
class Page_010_SelectComponents;
class Page_011_SelectLocation;
class Page_012_Instalation;
class Page_020_NameAndLocation;
class Page_013_Conclusion;
class Page_021_Options;
class Page_022_Creation;
class Page_023_Conclusion;

class MainWizard : public QWizard
{
    Q_OBJECT

public:
    enum {
        PAGE_000_WELCOME,
        PAGE_010_SELECTCOMPONENTS,
        PAGE_011_SELECTLOCATION,
        PAGE_012_INSTALATION,
        PAGE_013_CONCLUSION,

        PAGE_020_NAMEANDLOCATION,
        PAGE_021_OPTIONS,
        PAGE_022_CREATION,
        PAGE_023_CONCLUSION
    };


public:
    MainWizard();
    ~MainWizard();


private:
    Page_000_Welcome* m_page_000;

    Page_010_SelectComponents* m_page_010;
    Page_011_SelectLocation* m_page_011;
    Page_012_Instalation* m_page_012;
    Page_013_Conclusion* m_page_013;

    Page_020_NameAndLocation* m_page_020;
    Page_021_Options* m_page_021;
    Page_022_Creation* m_page_022;
    Page_023_Conclusion* m_page_023;
};
#endif // MAINWIZARD_H
