/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include "connectedview.h"

#include <QLabel>
#include <QHBoxLayout>
#include <QDebug>
#include <QBitmap>

#include <dthememanager.h>
#include <dseparatorhorizontal.h>

#include "constants.h"
#include "../helper.h"
#include "widgets/notifylabel.h"
#include "widgets/simplebutton.h"
#include "widgets/tiplabel.h"

DWIDGET_USE_NAMESPACE

ConnectedView::ConnectedView(QWidget* p)
    : AbstractView(p), m_text(new NotifyLabel(this))
{
    setObjectName("ConnectedView");
    initialize();
}

QWidget* ConnectedView::createMainWidget()
{
    auto mainWidget = new QWidget;
   // mainWidget->setFixedSize(DCC::ModuleContentWidth, 140);

    auto mainLayout = new QVBoxLayout(mainWidget);
    mainLayout->setSpacing(0);
    mainLayout->setMargin(0);

    m_text->setFixedSize(DRA::NotifyLabelMaxWidth, DRA::NotifyLabelMaxHeight);
    mainLayout->addSpacing(67);
    mainLayout->addWidget(m_text);
    mainLayout->addSpacing(30);

    TipLabel * tip  = new TipLabel(this);
    tip->setText(tr("Continue to access or disconnect"));
    tip->setFixedSize(DRA::TipLabelMaxWidth, DRA::TipLabelMaxHeight);
    mainLayout->addWidget(tip);

    auto button = new SimpleButton(tr("Disconnect"));
    connect(button, SIGNAL(clicked(bool)), this, SLOT(onDisconnectButtonClicked()));

    addButton(button);

    return mainWidget;
}

ConnectedView* ConnectedView::setText(const QString& text)
{
    m_text->setText(text);
    return this;
}

void ConnectedView::onDisconnectButtonClicked()
{
    emit disconnect();
}
