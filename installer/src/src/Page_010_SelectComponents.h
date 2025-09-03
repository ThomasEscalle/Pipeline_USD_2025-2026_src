#ifndef PAGE__1__SELECTCOMPONENTS_H
#define PAGE__1__SELECTCOMPONENTS_H

#include <QWizardPage>
#include <QTreeWidget>
#include <QMap>

namespace Ui {
class Page_010_SelectComponents;
}

class Page_010_SelectComponents : public QWizardPage
{
    Q_OBJECT

public:
    Page_010_SelectComponents();
    ~Page_010_SelectComponents();

    void createItems();
    
    // Méthode pour récupérer les composants sélectionnés
    QStringList getSelectedComponents() const;

    int nextId() const override;

private:
    Ui::Page_010_SelectComponents *ui;


    QMap<QString, QTreeWidgetItem*> m_items;
};

#endif // PAGE__1__SELECTCOMPONENTS_H
