#include "src/MainWizard.h"

#include "src/Page_000_Welcome.h"
#include "src/Page_010_SelectComponents.h"
#include "src/Page_011_SelectLocation.h"
#include "src/Page_012_Instalation.h"
#include "src/Page_013_Conclusion.h"

#include "src/Page_020_NameAndLocation.h"
#include "src/Page_021_Options.h"
#include "src/Page_022_Creation.h"
#include "src/Page_023_Conclusion.h"

#include "QAbstractButton"

MainWizard::MainWizard()
    : QWizard()
{
    setWizardStyle(WizardStyle::ModernStyle);
    
    // Disable the "Previous" button to prevent going back
    setOption(QWizard::NoBackButtonOnStartPage, true);
    setOption(QWizard::NoBackButtonOnLastPage, true);
    setOption(QWizard::DisabledBackButtonOnLastPage, true);
    

    /// Create the pages and add them
    m_page_000 = new Page_000_Welcome();
    setPage(PAGE_000_WELCOME , m_page_000);

    m_page_010 = new Page_010_SelectComponents();
    setPage(PAGE_010_SELECTCOMPONENTS, m_page_010);

    m_page_011 = new Page_011_SelectLocation();
    setPage(PAGE_011_SELECTLOCATION , m_page_011);

    m_page_012 = new Page_012_Instalation();
    setPage(PAGE_012_INSTALATION , m_page_012);

    m_page_013 = new Page_013_Conclusion();
    setPage(PAGE_013_CONCLUSION , m_page_013);

    m_page_020 = new Page_020_NameAndLocation();
    setPage(PAGE_020_NAMEANDLOCATION, m_page_020);

    m_page_021 = new Page_021_Options();
    setPage(PAGE_021_OPTIONS, m_page_021);

    m_page_022 = new Page_022_Creation();
    setPage(PAGE_022_CREATION, m_page_022);

    m_page_023 = new Page_023_Conclusion();
    setPage(PAGE_023_CONCLUSION, m_page_023);
}

MainWizard::~MainWizard() {}
