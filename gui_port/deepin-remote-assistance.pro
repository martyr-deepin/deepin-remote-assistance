TEMPLATE        = app

CONFIG         += plugin c++11 link_pkgconfig
QT             += widgets dbus x11extras svg
LIBS           += -lX11 -lXext
PKGCONFIG      += dtkbase dtkutil dtkwidget

HEADERS         = constants.h \
    controller/access.h \
    controller/share.h \
    interface.h \
    dbus/client.h \
    dbus/manager.h \
    dbus/server.h \
    remoteassistance.h \
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
    widgets/tiplabel.h \
    widgets/notifylabel.h \
    widgets/infolabel.h \
    widgets/diconbutton.h

SOURCES         = main.cpp \
    controller/share.cpp \
    controller/access.cpp \
    dbus/client.cpp \
    dbus/manager.cpp \
    dbus/server.cpp \
    remoteassistance.cpp \
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
    widgets/tiplabel.cpp \
    widgets/notifylabel.cpp \
    widgets/infolabel.cpp \
    widgets/diconbutton.cpp

TARGET          = deepin-remote-assistance
DESTDIR         = .
DISTFILES += light/button.theme \
    light/generatingview.theme \
    light/connectedview.theme \
    light/inputview.theme \
    light/generatedview.theme \
    light/errorview.theme \
    light/connectingview.theme \
    deepin-remote-assistance.desktop \
    TODO \
    light/WhiteButton.theme

#Automating generation .qm files from .ts files
system($$PWD/translate_generation.sh)

TRANSLATIONS = translations/deepin-remote-assistance.ts

qm_files.files = translations/*.qm
qm_files.path = /usr/share/deepin-remote-assistance/translations


RESOURCES += \
    theme.qrc \
    Resource.qrc
