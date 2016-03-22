#include "remoteassistance.h"


#include <QFrame>
#include <QApplication>
#include "constants.h"

int main(int argv, char *args[])
{
    QApplication app(argv, args);
    app.setOrganizationName("deepin");
    app.setApplicationName("deepin-remote-assistance");
    app.setApplicationVersion("1.0");
    DRA::globalApp = &app;


    RemoteAssistance ra;
    ra.showWindow();
    DRA::globalRa = &ra;



    return app.exec();
}
