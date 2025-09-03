#ifndef EXPORTTEXTUREMAINWINDOW_H
#define EXPORTTEXTUREMAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui {
class ExportTextureMainWindow;
}
QT_END_NAMESPACE

class ExportTextureMainWindow : public QMainWindow
{
    Q_OBJECT

public:
    ExportTextureMainWindow(QWidget *parent = nullptr);
    ~ExportTextureMainWindow();

private:
    Ui::ExportTextureMainWindow *ui;
};
#endif // EXPORTTEXTUREMAINWINDOW_H
