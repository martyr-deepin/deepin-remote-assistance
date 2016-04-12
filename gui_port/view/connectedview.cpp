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
#include "widgets/simplebutton.h"

#include "constants.h"

#include "../helper.h"

DWIDGET_USE_NAMESPACE

ConnectedView::ConnectedView(QWidget* p)
    : AbstractView(p), m_text(new QLabel)
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


    auto button = new SimpleButton(tr("断开"));
    connect(button, SIGNAL(clicked(bool)), this, SLOT(onDisconnectButtonClicked()));

    m_text->setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    m_text->setFixedSize(DRA::ModuleContentWidth, 70);
    m_text->setAlignment(Qt::AlignCenter);
    m_text->setWordWrap(true);

    QLabel * msgBox = new QLabel;
        msgBox->setText("您可以继续访问或选择断开");
        msgBox->setStyleSheet("font-size:10px;"
                              "color:#848484;");
    //    mainLayout->addSpacing(10);

    mainLayout->addWidget(m_text, 0, Qt::AlignCenter);
    mainLayout->addWidget(msgBox, 0, Qt::AlignCenter);
    mainLayout->addWidget(button, 0, Qt::AlignCenter);


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
