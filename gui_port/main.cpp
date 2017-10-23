#include "remoteassistance.h"


#include <QFrame>
#include <DApplication>
#include <DLog>

#include "constants.h"

DCORE_USE_NAMESPACE
DWIDGET_USE_NAMESPACE

int main(int argv, char *args[])
{
    DApplication::loadDXcbPlugin();

    DApplication app(argv, args);
    app.setAttribute(Qt::AA_UseHighDpiPixmaps);
    app.setAttribute(Qt::AA_EnableHighDpiScaling);
    app.setOrganizationName("deepin");
    app.setApplicationName("deepin-remote-assistance");
    app.setApplicationVersion("1.0");
    app.setTheme("light");
    app.loadTranslator();

    app.setProductName(QApplication::translate("Impl", "Remote Assistance"));
    app.setProductIcon(QIcon(":/resource/theme/images/deepin-remote-assistance.svg"));
    app.setApplicationDescription(QApplication::translate("Impl", "Remote Assistance is a remote controller, users can connect to computers between each other with it."));

    DLogManager::registerConsoleAppender();

    if (!app.setSingleInstance("deepin-remote-assistance-ui")) {
        qDebug() << "Another deepin-remote-assistance exist.";
        return 0;
    }

    RemoteAssistance ra;
    QObject::connect(&app, SIGNAL(aboutToQuit()), &ra, SIGNAL(aboutToQuit()));

    ra.showWindow();

    return app.exec();
}
