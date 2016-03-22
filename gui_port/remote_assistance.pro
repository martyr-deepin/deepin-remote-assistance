TEMPLATE        = app

CONFIG         += plugin c++11 link_pkgconfig
QT             += widgets dbus x11extras svg
LIBS           += -lX11 -lXext
PKGCONFIG      += dtkbase dtkwidget

HEADERS         = constants.h \
    moduleheader.h \
    controller/access.h \
    controller/share.h \
    interface.h \
    dbus/client.h \
    dbus/manager.h \
    dbus/server.h \
    remoteassistance.h \
    view/buttongroup.h \
    view/button.h \
    view/abstractpanel.h \
    view/sharepanel.h \
    view/mainpanel.h \
    view/accesspanel.h \
    view/generatingview.h \
    view/generatedview.h \
    view/errorview.h \
    view/connectedview.h \
    view/connectingview.h \
    view/inputview.h \
    view/abstractview.h \
    helper.h \
    dmovie.h \
    view/ddraging.h

SOURCES         = main.cpp \
    moduleheader.cpp \
    controller/share.cpp \
    controller/access.cpp \
    dbus/client.cpp \
    dbus/manager.cpp \
    dbus/server.cpp \
    remoteassistance.cpp \
    view/buttongroup.cpp \
    view/button.cpp \
    view/abstractpanel.cpp \
    view/accesspanel.cpp \
    view/mainpanel.cpp \
    view/sharepanel.cpp \
    view/generatingview.cpp \
    view/generatedview.cpp \
    view/errorview.cpp \
    view/connectedview.cpp \
    view/connectingview.cpp \
    view/abstractview.cpp \
    view/inputview.cpp \
    helper.cpp \
    dmovie.cpp \
    view/ddraging.cpp

TARGET          = $$qtLibraryTarget(remote_assistance) # ??
DESTDIR         = .
DISTFILES += dark/button.theme \
    dark/generatingview.theme \
    dark/connectedview.theme \
    dark/inputview.theme \
    dark/generatedview.theme \
    dark/errorview.theme \
    dark/connectingview.theme \
    deepin-remote-assistance.desktop \
    TODO

RESOURCES += \
    theme.qrc
