/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include <QFrame>
#include <QDBusConnection>
#include <QVBoxLayout>
#include <QIcon>
#include <QMenu>
#include <QAction>

#include <DWindow>
#include <dstackwidget.h>

#include "remoteassistance.h"
#include "dbus/manager.h"
#include "controller/access.h"
#include "controller/share.h"
#include "view/accesspanel.h"
#include "view/mainpanel.h"
#include "view/sharepanel.h"
#include "constants.h"
#include "helper.h"
#include <DAboutDialog>

namespace ManagerState
{
enum {
    Uninitialized,
    Client,
    Server,
};
}

DWIDGET_USE_NAMESPACE

Impl::Impl(RemoteAssistance *pub, com::deepin::daemon::Remoting::Manager *manager)
    : m_pub(pub),
      m_manager(manager),
      m_view(new DWindow),
      m_stackWidget(new DStackWidget)
{
    QVBoxLayout *mainLayout = new QVBoxLayout;
    mainLayout->setMargin(0);
    mainLayout->setSpacing(0);

    m_view->setTitle(tr("Remote Assistance"));

    QSize frameSize(DRA::WindowWidth, DRA::WindowHeight);
    QSize contentSize(DRA::WindowWidth,
                      DRA::WindowHeight - m_view->titlebarHeight());

    QAction *aboutAction = new QAction(tr("About"), this);
    connect(aboutAction, SIGNAL(triggered()), this, SLOT(showAbout()));

    QAction *helpAction = new QAction(tr("Help"), this);
    connect(helpAction, SIGNAL(triggered()), this, SLOT(showHelp()));

    QAction *closeAction = new QAction(tr("Exit"), this);
    connect(closeAction, SIGNAL(triggered()), m_view, SLOT(close()));

    m_view->titleBarMenu()->addAction(aboutAction);
    m_view->titleBarMenu()->addAction(helpAction);
    m_view->titleBarMenu()->addAction(closeAction);

    m_view->setWindowFlags(m_view->windowFlags() & ~ Qt::WindowMaximizeButtonHint);
    m_view->setFixedSize(frameSize);
    m_view->setBackgroundColor(Qt::white);

    m_stackWidget->setFixedSize(contentSize);
    mainLayout->addWidget(m_stackWidget/*, 0, Qt::AlignHCenter*/);

    m_view->setContentLayout(mainLayout);

    connect(m_stackWidget->transition()->animation(), SIGNAL(finished()), pub, SLOT(onAnimationEnd()));

    qApp->installEventFilter(this);
}

Impl::~Impl()
{
    m_manager->deleteLater();
}

void Impl::showAbout()
{
    QString descriptionText = tr("Remote Assistance is a remote controller, users can connect to computers between each other with it.");

    DAboutDialog *about = new DAboutDialog(m_view);
    about->setProductName(tr("Remote Assistance"));
    about->setProductIcon(QPixmap(":/Resource/remote-assistance-96.png"));
    about->setVersion(tr("Version: %1").arg(qApp->applicationVersion()));
    about->setDescription(descriptionText);
    about->setLicense(tr("Deepin Remote Assistance is released under GPL v3"));
    about->setAcknowledgementLink("https://www.deepin.org/acknowledgments/deepin-remote-assistance");

    about->show();
}


void Impl::showHelp()
{
    if (NULL == dManual) {
        dManual =  new QProcess(this);
        const QString pro = "dman";
        const QStringList args("deepin-remote-assistance");
        connect(dManual, SIGNAL(finished(int)), this, SLOT(manualClose(int)));
        dManual->start(pro, args);
    }
}


void Impl::initPanel()
{
    qDebug() << "initPanel";
    QDBusPendingReply<int> reply = m_manager->GetStatus();
    reply.waitForFinished();
    if (reply.isError()) {
        qDebug() << reply.error();
        return ;
    }
    qDebug() << reply.value();
    pushView(getPanel(ViewPanel::Main), false);
    switch (reply.value()) {
    case ManagerState::Uninitialized:
        m_viewType = ViewPanel::Main;
        break;
    case ManagerState::Client:
        m_viewType = ViewPanel::Access;
        pushView(getPanel(ViewPanel::Access), false);
        break;
    case ManagerState::Server:
        m_viewType = ViewPanel::Share;
        pushView(getPanel(ViewPanel::Share), false);
        break;
    }
}

void Impl::debug()
{
    this->m_view->showMinimized();
}

bool Impl::eventFilter(QObject *obj, QEvent *event)
{
    if (event->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);
        if (keyEvent->key() == Qt::Key_F1) {
            qDebug() << "show manual for help...";
            showHelp();
            return true;
        }
    }
    // standard event processing
    return QObject::eventFilter(obj, event);
}

void Impl::manualClose(int)
{
    dManual->deleteLater();
    dManual = NULL;
}

QWidget *Impl::getPanel(ViewPanel v)
{
    switch (v) {
    case ViewPanel::Main: {
        // MainPanel should be created only once.
        qDebug() << "create Main Panel";
        m_mainPanel = new MainPanel(m_manager);
        QObject::connect(m_mainPanel, SIGNAL(changePanel(ViewPanel)), m_pub, SLOT(changePanel(ViewPanel)));

        return m_mainPanel;
    }
    case ViewPanel::Access: {
        qDebug() << "create Access Panel";
        auto client = new com::deepin::daemon::Remoting::Client("com.deepin.daemon.Remoting.Client", "/com/deepin/daemon/Remoting/Client", QDBusConnection::sessionBus());
        auto controller = new AccessController(m_manager, client);
        m_accessPanel = new AccessPanel(controller);
        QObject::connect(m_pub, SIGNAL(aboutToQuit()), (AccessPanel *)m_accessPanel, SLOT(emitChangePanel()));
        QObject::connect(m_accessPanel, SIGNAL(changePanel(ViewPanel)), m_pub, SLOT(changePanel(ViewPanel)));
        QObject::connect(m_accessPanel, SIGNAL(connected()), this, SLOT(debug()));
        return m_accessPanel;
    }
    case ViewPanel::Share: {
        qDebug() << "create Share Panel";
        auto server = new com::deepin::daemon::Remoting::Server("com.deepin.daemon.Remoting.Server", "/com/deepin/daemon/Remoting/Server", QDBusConnection::sessionBus());
        auto controller  = new ShareController(m_manager, server);
        m_sharePanel = new SharePanel(controller);
        QObject::connect(m_pub, SIGNAL(aboutToQuit()), (SharePanel *)m_sharePanel, SLOT(onDisconnected()));
        QObject::connect(m_sharePanel, SIGNAL(changePanel(ViewPanel)), m_pub, SLOT(changePanel(ViewPanel)));
        return m_sharePanel;
    }
    }
    throw "[RemoteAssistance::Impl::getPanel] should not reach here";
}

void Impl::changeTitle(ViewPanel v)
{
    switch (v) {
    case ViewPanel::Main: {
        // MainPanel should be created only once.
        m_view->setTitle(tr("Remote Assistance"));
        qDebug() << "height" << m_view->height();
        m_view->setTitleIcon(QPixmap());
        break;

    }
    case ViewPanel::Access: {
        qDebug() << "create Access Panel";
        m_view->setTitle(tr("Assist others"));
        m_view->setTitleIcon(QPixmap(getThemeImage("assistant_heart.png")));
        break;

    }
    case ViewPanel::Share: {
        qDebug() << "create Share Panel";
        m_view->setTitle(tr("Assist me"));
        m_view->setTitleIcon(QPixmap(getThemeImage("assistant_help.png")));
        break;
    }
    }
}

void Impl::changePanel(ViewPanel v)
{
    qDebug() << "changePanel to " << v;
    qDebug() << "m_stackWidget->depth()" << m_stackWidget->depth();
    m_viewType = v;
    changeTitle(v);
    while (m_stackWidget->depth() > 1) {
        popView();
        qDebug() << "popView return";
        return;
    }

    QWidget *panel = getPanel(v);

    qDebug() << "old panel" << m_panel->objectName();

    pushView(panel);

    qDebug() << "current panel" << m_panel->objectName();
}

void RemoteAssistance::onAnimationEnd()
{
    qDebug() << "onAnimationEnd();";
    AccessPanel *m_accessPanel = qobject_cast<AccessPanel *>(m_impl->m_panel);
    if (m_accessPanel) {
        m_accessPanel->focus();
    }
}

void RemoteAssistance::changePanel(ViewPanel v)
{
    qDebug() << "changePanel" << v;
    m_impl->changePanel(v);
}

inline void Impl::pushView(QWidget *w, bool enableTransition)
{
    m_panel = w;
    m_stackWidget->pushWidget(w, enableTransition);
}

inline void Impl::popView(QWidget *w, bool isDelete, int count, bool enableTransition)
{
//    qDebug() << "pop last panel" << m_panel->objectName() << ", depth" << m_stackWidget->depth();
    m_stackWidget->popWidget(w, isDelete, count, enableTransition);
    m_panel = m_stackWidget->currentWidget();
//    qDebug() << "current panel is" << m_panel->objectName();
}

RemoteAssistance::RemoteAssistance()
    : QObject(),
      m_impl(new Impl(this,
                      new com::deepin::daemon::Remoting::Manager("com.deepin.daemon.Remoting.Manager",
                              "/com/deepin/daemon/Remoting/Manager",
                              QDBusConnection::sessionBus()
                                                                )
                     ))

{

    m_impl->initPanel();

}

RemoteAssistance::~RemoteAssistance()
{
}

void RemoteAssistance::showWindow()
{
    m_impl->m_view->show();
}


void RemoteAssistance::hide()
{

}

