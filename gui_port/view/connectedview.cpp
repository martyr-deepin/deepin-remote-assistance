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

#include <libdui/dthememanager.h>
#include <dseparatorhorizontal.h>
#include <dtextbutton.h>

#include "constants.h"

#include "../helper.h"

DUI_USE_NAMESPACE

ConnectedView::ConnectedView(QWidget* p)
    : AbstractView(p), m_text(new QLabel)
{
    setObjectName("ConnectedView");
    initialize();



    setStyleSheet(readStyleSheet("connectedview"));
}

QWidget* ConnectedView::createMainWidget()
{
    auto mainWidget = new QWidget;
   // mainWidget->setFixedSize(DCC::ModuleContentWidth, 140);

    auto mainLayout = new QVBoxLayout(mainWidget);
    mainLayout->setSpacing(0);
    mainLayout->setMargin(0);


    auto button = new DTextButton(tr("Disconnect"));
    connect(button, SIGNAL(clicked(bool)), this, SLOT(onDisconnectButtonClicked()));


    QPixmap pixmap(getThemeImage("blue_button_normal.png"));
    QPalette   pal;
    pal.setColor(QPalette::ButtonText, QColor(255,255,255));
    button->setMask(pixmap.mask());
    button->setStyleSheet("QPushButton{border-image:url(" + getThemeImage("blue_button_normal.png") + ");}"
                         "QPushButton:hover{border-image:url("+ getThemeImage("button_hover.png") + ");}"
                         "QPushButton:pressed{border-image:url(" + getThemeImage("button_press.png") +");}");
    button->setFixedSize(120, 32);
    button->setPalette(pal);





    m_text->setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    m_text->setFixedSize(DCC::ModuleContentWidth, 70);
    m_text->setAlignment(Qt::AlignCenter);
    m_text->setWordWrap(true);

    mainLayout->addWidget(m_text, 0, Qt::AlignHCenter);
    mainLayout->addWidget(button, 0, Qt::AlignHCenter);


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
