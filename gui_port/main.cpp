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


    QTranslator translator;
    translator.load("/usr/share/dde-launcher/translations/deepin-remote-assistance_" +
    QLocale::system().name() + ".qm");
    app.installTranslator(&translator);

    RemoteAssistance ra;
    ra.showWindow();
    DRA::globalRa = &ra;



    return app.exec();
}
