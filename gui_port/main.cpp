#include "remoteassistance.h"

#include <QFrame>
#include <QApplication>

int main(int argv, char *args[])
{
    QApplication app(argv, args);
    app.setOrganizationName("deepin");
    app.setApplicationName("deepin-remote-assistance");
    app.setApplicationVersion("1.0");

    RemoteAssistance ra;
    ra.getContent()->show();

    return app.exec();
}
