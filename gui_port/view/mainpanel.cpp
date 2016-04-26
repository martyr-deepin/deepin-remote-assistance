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
#include <QMouseEvent>
#include <dseparatorhorizontal.h>
#include <QPushButton>
#include <QSvgWidget>

#include <dbasebutton.h>

#include "constants.h"
#include "mainpanel.h"
#include "helper.h"
#include "widgets/tiplabel.h"

DWIDGET_USE_NAMESPACE

MainPanel::MainPanel(com::deepin::daemon::Remoting::Manager *manager, QWidget *p):
    AbstractPanel(tr(" "), p)
{
    setObjectName("MainPanel");
    m_manager = manager;

    auto mainWidget = new QWidget;
    mainWidget->setStyleSheet("QWidget { background-color: #f5f5f8 }");

    auto mainLayout = new QVBoxLayout(mainWidget);
    mainLayout->setSpacing(0);
    mainLayout->setMargin(0);


    QSvgWidget *picon = new QSvgWidget(getThemeImage("logo.svg"));

    picon->setContentsMargins(0, 0, 0, 0);
    picon->setFixedSize(64, 64);
    mainLayout->addSpacing(18);
    mainLayout->addWidget(picon, 0, Qt::AlignHCenter);


    TipLabel *ptext = new TipLabel(this);
    ptext->setText(tr("Welcome to Remote Assistance, users can fix computer issues between each other with it."));
    ptext->setFixedSize(DRA::TipLabelMaxWidth, DRA::TipLabelMaxHeight);

    mainLayout->addSpacing(137 - (64 + 50));
    mainLayout->addWidget(ptext, 0 , Qt::AlignCenter);

    DBaseButton *button = nullptr;
    button = new DBaseButton;
    button->setFixedSize(160, 36);

    QFile btTheme(":/dark/WhiteButton.theme");
    btTheme.open(QIODevice::ReadOnly);
    QString btThemeStr = btTheme.readAll();
    btTheme.close();

    button->setText("  " + tr("Assist me"));
    button->setIcon(QIcon(getThemeImage("assistant_help.png")));
    button->setStyleSheet(btThemeStr);
    mainLayout->addSpacing(198 - (40 + 23 + 64 + 50));
    mainLayout->addWidget(button, 0, Qt::AlignCenter);

    connect(button, SIGNAL(clicked()), this, SLOT(changeToSharePanel()));

    button = new DBaseButton;
    button->setFixedSize(160, 36);
    button->setText("  " + tr("Assist others"));
    button->setIcon(QIcon(getThemeImage("assistant_heart.png")));
    button->setStyleSheet(btThemeStr);

    connect(button, SIGNAL(clicked()), this, SLOT(changeToAccessPanel()));

    mainLayout->addSpacing(244 - (198 + 36));
    mainLayout->addWidget(button, 0, Qt::AlignCenter);
    mainLayout->addStretch();
    this->setLayout(mainLayout);
    setWidget(mainWidget);

}

void MainPanel::emitPanelChanged(ViewPanel v)
{
    qDebug() << "emitPanelChanged";
    emit changePanel(v);
}

void MainPanel::changeToAccessPanel()
{
    emitPanelChanged(ViewPanel::Access);
}

void MainPanel::changeToSharePanel()
{
    emitPanelChanged(ViewPanel::Share);
}
