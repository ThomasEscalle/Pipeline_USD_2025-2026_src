#include "src/Page_010_SelectComponents.h"
#include "ui_Page_010_SelectComponents.h"

#include "MainWizard.h"

Page_010_SelectComponents::Page_010_SelectComponents()
    : QWizardPage()
    , ui(new Ui::Page_010_SelectComponents)
{
    ui->setupUi(this);

    // Title and subtitle
    setTitle(tr("Select Components"));
    setSubTitle(tr("Select the components you want to install."));
    setPixmap(QWizard::LogoPixmap, QPixmap(":/icons/ICON_64.png"));

    createItems();
}

Page_010_SelectComponents::~Page_010_SelectComponents()
{
    delete ui;
}

void Page_010_SelectComponents::createItems()
{
    ui->treeWidget->clear();
    /// Create a root tree widget for "Prism"
    QTreeWidgetItem* rootItem = new QTreeWidgetItem(ui->treeWidget);
    rootItem->setText(0, "Prism");
    m_items["Prism"] = rootItem;
    ui->treeWidget->addTopLevelItem(rootItem);

    /// Add a "Main prism plugin" item, checkable
    QTreeWidgetItem* mainPluginItem = new QTreeWidgetItem(rootItem);
    mainPluginItem->setText(0, "Main prism plugin");
    mainPluginItem->setCheckState(0, Qt::Checked);
    m_items["Main prism plugin"] = mainPluginItem;

    /// Add a "Zbrush prim plugin" item, checkable
    QTreeWidgetItem* zbrushPluginItem = new QTreeWidgetItem(rootItem);
    zbrushPluginItem->setText(0, "Zbrush prim plugin");
    zbrushPluginItem->setCheckState(0, Qt::Checked);
    m_items["Zbrush prim plugin"] = zbrushPluginItem;

    /// Add a "Substance painter plugin" item, checkable
    QTreeWidgetItem* substancePluginItem = new QTreeWidgetItem(rootItem);
    substancePluginItem->setText(0, "Substance painter plugin");
    substancePluginItem->setCheckState(0, Qt::Checked);
    m_items["Substance painter plugin"] = substancePluginItem;



    /// Create a root tree widget for "Maya"
    QTreeWidgetItem* mayaRootItem = new QTreeWidgetItem(ui->treeWidget);
    mayaRootItem->setText(0, "Maya");
    m_items["Maya"] = mayaRootItem;
    ui->treeWidget->addTopLevelItem(mayaRootItem);

    /// Add a "Save as script" item, checkable  
    QTreeWidgetItem* saveAsScriptItem = new QTreeWidgetItem(mayaRootItem);
    saveAsScriptItem->setText(0, "Save as script");
    saveAsScriptItem->setCheckState(0, Qt::Checked);
    m_items["Save as script Maya"] = saveAsScriptItem;

    /// Add a "Shelf" item checkable
    QTreeWidgetItem* shelfItem = new QTreeWidgetItem(mayaRootItem);
    shelfItem->setText(0, "Shelf");
    shelfItem->setCheckState(0, Qt::Checked);
    m_items["Shelf Maya"] = shelfItem;

    /// Add a "Maya Asset Browser" item checkable   
    QTreeWidgetItem* assetBrowserItem = new QTreeWidgetItem(mayaRootItem);
    assetBrowserItem->setText(0, "Maya Asset Browser");
    assetBrowserItem->setCheckState(0, Qt::Checked);
    m_items["Maya Asset Browser"] = assetBrowserItem;
    
    /// Add a "Maya shot manager" item checkable
    QTreeWidgetItem* shotManagerItem = new QTreeWidgetItem(mayaRootItem);
    shotManagerItem->setText(0, "Maya shot manager");
    shotManagerItem->setCheckState(0, Qt::Checked);
    m_items["Maya shot manager"] = shotManagerItem;


    /// Create a root tree widget for "Houdini"
    QTreeWidgetItem* houdiniRootItem = new QTreeWidgetItem(ui->treeWidget);
    houdiniRootItem->setText(0, "Houdini");
    m_items["Houdini"] = houdiniRootItem;
    ui->treeWidget->addTopLevelItem(houdiniRootItem);

    /// Add a "Houdini Asset browser" item checkable
    QTreeWidgetItem* houdiniAssetBrowserItem = new QTreeWidgetItem(houdiniRootItem);
    houdiniAssetBrowserItem->setText(0, "Houdini Asset Browser");
    houdiniAssetBrowserItem->setCheckState(0, Qt::Checked);
    m_items["Houdini Asset Browser"] = houdiniAssetBrowserItem;


    /// Add a "Houdini custom nodes" item checkable
    QTreeWidgetItem* houdiniCustomNodesItem = new QTreeWidgetItem(houdiniRootItem);
    houdiniCustomNodesItem->setText(0, "Houdini Custom nodes");
    houdiniCustomNodesItem->setCheckState(0, Qt::Checked);
    m_items["Houdini custom nodes"] = houdiniCustomNodesItem;



    /// todo
    /// ...



    /// Unfold all items
    ui->treeWidget->expandAll();
}

QStringList Page_010_SelectComponents::getSelectedComponents() const
{
    QStringList selectedComponents;
    
    for (auto it = m_items.begin(); it != m_items.end(); ++it) {
        QTreeWidgetItem* item = it.value();
        // Vérifier si l'item est coché et n'est pas un item racine
        if (item->checkState(0) == Qt::Checked && item->parent() != nullptr) {
            selectedComponents.append(it.key());
        }
    }
    
    return selectedComponents;
}


int Page_010_SelectComponents::nextId() const
{
    return MainWizard::PAGE_011_SELECTLOCATION;
}

void Page_010_SelectComponents::on_uncheckAll_clicked()
{
    for (auto it = m_items.begin(); it != m_items.end(); ++it) {
        QTreeWidgetItem* item = it.value();
        // Vérifier si l'item est coché et n'est pas un item racine
        if (item->checkState(0) == Qt::Checked && item->parent() != nullptr) {
            item->setCheckState(0, Qt::Unchecked);
        }
    }
}

