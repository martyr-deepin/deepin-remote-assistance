/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include <QLabel>
#include <QVBoxLayout>
#include <QBitmap>

#include "accesspanel.h"
#include <dbasebutton.h>

#include "connectingview.h"
#include "connectedview.h"
#include "errorview.h"
#include "inputview.h"
#include "constants.h"
#include "helper.h"

DWIDGET_USE_NAMESPACE

AccessPanel::AccessPanel(IAccessController *controller, QWidget *p)
    : AbstractPanel(tr("Assist me"), p),
      m_controller(controller)
{
    setObjectName("AccessPanel");
    connect(controller, SIGNAL(noNetwork()), this, SLOT(onNoNetwork()));
    connect(controller, SIGNAL(connected()), this, SLOT(onConnected()));
    connect(controller, SIGNAL(stopped()), this, SLOT(onStopped()));

    if (controller->isAlreadyConnected()) {
        onConnected();
        return;
    }

    m_inputView = new InputView;
    connect(m_inputView, SIGNAL(connect(QString)), this, SLOT(onConnect(QString)));
    connect(m_inputView, SIGNAL(cancel()), this, SLOT(onDisconnected()));
    setWidget(m_inputView);

    connect(controller, SIGNAL(connecting()), this, SLOT(onConnecting()));
    connect(controller, SIGNAL(connectFailed(AccessErrors)), this, SLOT(onConnectFailed(AccessErrors)));
    controller->initStatus();

    m_controller->setParent(this);
}

AccessPanel::~AccessPanel()
{
    m_controller->disconnect();
}

void AccessPanel::emitChangePanel()
{
    emit changePanel(ViewPanel::Main);
}

void AccessPanel::onStopped()
{
    qDebug() << "onStopped";
//    emitChangePanel();
}

void AccessPanel::abort()
{
    onDisconnected();
}

void AccessPanel::onConnect(QString token)
{
    m_controller->connect(token);
    onConnecting();
}

void AccessPanel::onConnecting()
{
    qDebug() << "connecting";
    auto view = new ConnectingView;
    connect(view, SIGNAL(cancel()), this, SLOT(onDisconnected()));
    setWidget(view);
}

void AccessPanel::onConnected()
{
    qDebug() << "connected";
    auto view = new ConnectedView;
    view->setText(tr("Remotely assisting"));
    connect(view, SIGNAL(disconnect()), this, SLOT(onDisconnected()));
    setWidget(view);
    connect(m_controller, SIGNAL(disconnected()), this, SLOT(onDisconnected()));
    emit connected();
}

void AccessPanel::onConnectFailed(AccessErrors e)
{
    qDebug() << "connect failed";
    auto view = new ErrorView;
    switch (e) {
    case AccessError::ConnectServerFailed:
        qDebug() << "connect server failed";
        break;
    case AccessError::InvalidToken:
        qDebug() << "invalid token";
        auto inputView = new InputView;
        connect(inputView, SIGNAL(connect(QString)), this, SLOT(onConnect(QString)));
        connect(inputView, SIGNAL(cancel()), this, SLOT(onDisconnected()));
        inputView->setTips(tr("Invalid verification code, please retry!"));
        setWidget(inputView);
        return;
    }

    view->setText(tr("Connect failed"))->setTips(tr("Failed to establish connection, please retry"));

    auto button = new Dtk::Widget::DBaseButton(tr("Cancel"));
    button->setFixedSize(160, 36);
    connect(button, &Dtk::Widget::DBaseButton::clicked, [this] {
        emitChangePanel();
    });
    view->addButton(button, 0, Qt::AlignCenter);

    button = new Dtk::Widget::DBaseButton(tr("Retry"));
    button->setFixedSize(160, 36);
    button->setEnabled(false);

    // waiting the remoting window to be closed.
    // NB: QTimer::singleShot not support lambda in Qt5.3.
    auto timer = new QTimer(this); // FIXME: this timer may not needed now.
    timer->setInterval(200);
    timer->setSingleShot(true);
    QObject::connect(timer, &QTimer::timeout, [ = ] {
        qDebug() << "enable retry button";
        button->setEnabled(true);
        timer->deleteLater();
    });
    timer->start();
    connect(button, &Dtk::Widget::DBaseButton::clicked, [this] {
        m_controller->retry();
    });
    view->addButton(button, 0, Qt::AlignCenter);

    setWidget(view);
}

void AccessPanel::onDisconnected()
{
    qDebug() << "disconnected accessing";
    m_controller->disconnect();
    emitChangePanel();
}

void AccessPanel::focus()
{
    InputView *inputView = qobject_cast<InputView *>(m_view);
    if (inputView) {
        inputView->focus();
    }
}
