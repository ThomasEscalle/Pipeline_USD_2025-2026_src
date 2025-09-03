#include "src/MainWizard.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWizard w;
    w.show();
    return a.exec();
}
