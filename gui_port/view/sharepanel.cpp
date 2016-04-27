/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include <QLabel>
#include <dseparatorhorizontal.h>
#include <dbasebutton.h>

#include "constants.h"

#include "sharepanel.h"
#include "interface.h"
#include "generatingview.h"
#include "generatedview.h"
#include "connectedview.h"
#include "errorview.h"

DWIDGET_USE_NAMESPACE

SharePanel::SharePanel(IShareController *controller, QWidget *p)
    : AbstractPanel(tr(" "), p),
      m_controller(controller)
{
    setObjectName("SharePanel");
//    connect(controller, SIGNAL(noNetwork()), this, SLOT(onGenAccessTokenFailed()));
//    connect(controller, SIGNAL(stopped()), this, SLOT(onStop()));
    m_deleyRetryTimer = new QTimer(this);
    connect(m_deleyRetryTimer, &QTimer::timeout, this, &SharePanel::onRetry);
    if (controller->isSharing()) {
        onSharing();
        return;
    }

    connect(controller, SIGNAL(sharing()), this, SLOT(onSharing()));
    connect(controller, SIGNAL(generatingAccessToken()), this, SLOT(onGeneratingAccessToken()));
    connect(controller, SIGNAL(disconnected()), this, SLOT(onDisconnected()));
    connect(controller, SIGNAL(genAccessTokenFailed()), this, SLOT(onGenAccessTokenFailed()));
    connect(controller, SIGNAL(genAccessTokenSuccessed(QString)), this, SLOT(onGenAccessTokenSuccessed(QString)));
    controller->startGenAccessToken();
}

SharePanel::~SharePanel()
{
    dtor();
}


void SharePanel::dtor()
{
    if (m_controller != nullptr) {
        m_controller->deleteLater();
        m_controller = nullptr;
    }
}

void SharePanel::emitChangePanel()
{
    dtor();
    qDebug() << "emit changePanel";
    emit changePanel(ViewPanel::Main);
}

void SharePanel::abort()
{
    onDisconnected();
    emitChangePanel();
}

void SharePanel::onStop()
{
    emitChangePanel();
}

void SharePanel::onSharing()
{
    qDebug() << "sharing";
    auto view = new ConnectedView;
    view->setText(tr("Remotely assisting"));
    connect(view, SIGNAL(disconnect()), this, SLOT(onDisconnectedWithAsk()));
    setWidget(view);
}

void SharePanel::onGeneratingAccessToken()
{
    qDebug() << "generating access token";
    auto view = new GeneratingView;
    connect(view, SIGNAL(cancel()), this, SLOT(onDisconnected()));
    setWidget(view);
}

void SharePanel::onDisconnectedWithAsk()
{
    qDebug() << "onDisconnectedWithAsk";
    m_controller->disconnect();
}

void SharePanel::onDisconnected()
{
    qDebug() << "disconnect immedately" << m_controller->isSharing();
    m_controller->cancel();
    emitChangePanel();
}

void SharePanel::onGenAccessTokenFailed()
{
    qDebug() << "gen access token failed";
    auto view = new ErrorView;

    auto button = new DBaseButton(tr("Retry"));
    button->setFixedSize(160, 36);
    QObject::connect(button, &DBaseButton::clicked, [this] {
        onGeneratingAccessToken();
        m_deleyRetryTimer->start(2000);
    });
    view->addButton(button);

    setWidget(view->setText(tr("Connected failed"))->setTips(tr("Failed to obtain verification code! ")));
}


void SharePanel::onRetry()
{
    qDebug() << "SharePanel::OnRetry()";
    m_deleyRetryTimer->stop();
    m_controller->startGenAccessToken();
}

void SharePanel::onGenAccessTokenSuccessed(QString token)
{
    qDebug() << "gen access token done";
    auto view = new GeneratedView(token);
    //connect(
    connect(view, SIGNAL(cancel()), this, SLOT(onDisconnected()));
    view->show();
    setWidget(view);
}
