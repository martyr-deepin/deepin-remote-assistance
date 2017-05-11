#include "remoteassistance.h"


#include <QFrame>
#include <DApplication>
#include <DLog>

#include "constants.h"

using namespace Dtk::Widget;
using namespace Dtk::Util;

int main(int argv, char *args[])
{
    DApplication::loadDXcbPlugin();

    DApplication app(argv, args);

    app.setOrganizationName("deepin");
    app.setApplicationName("deepin-remote-assistance");
    app.setApplicationVersion("1.0");
    app.setTheme("light");

    DLogManager::registerConsoleAppender();

    if (!app.setSingleInstance("deepin-remote-assistance-ui")) {
        qDebug() << "Another deepin-remote-assistance exist.";
        return 0;
    }

    app.loadTranslator();

    RemoteAssistance ra;
    QObject::connect(&app, SIGNAL(aboutToQuit()), &ra, SIGNAL(aboutToQuit()));

    ra.showWindow();

    return app.exec();
}
