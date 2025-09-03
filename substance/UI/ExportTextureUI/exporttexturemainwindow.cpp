#include "exporttexturemainwindow.h"
#include "./ui_exporttexturemainwindow.h"

ExportTextureMainWindow::ExportTextureMainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::ExportTextureMainWindow)
{
    ui->setupUi(this);
}

ExportTextureMainWindow::~ExportTextureMainWindow()
{
    delete ui;
}
