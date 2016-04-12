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

#include "constants.h"

#include "mainpanel.h"
#include "buttongroup.h"
#include "button.h"
#include "helper.h"

DWIDGET_USE_NAMESPACE

MainPanel::MainPanel(com::deepin::daemon::Remoting::Manager* manager, QWidget*p): AbstractPanel(tr(" "), p), m_buttongroup(new ButtonGroup)
{
    setObjectName("MainPanel");
    m_manager = manager;

    // addWidget(new DSeparatorHorizontal);
    // m_buttongroup->setGroupTitle(tr("Remote Assistance"));


    setWindowTitle("远程协助");

    auto mainWidget = new QWidget;
    mainWidget->setStyleSheet("QWidget { background-color: #f5f5f8 }");

    auto mainLayout = new QVBoxLayout(mainWidget);
    mainLayout->setSpacing(0);
    mainLayout->setMargin(0);


    QSvgWidget *picon = new QSvgWidget(getThemeImage("logo.svg"));

    picon->setContentsMargins(0,0,0,0);
    picon->setFixedSize(64,64);
    mainLayout->addSpacing(18);
    mainLayout->addWidget(picon, 0, Qt::AlignHCenter);


    QLabel *ptext = new QLabel;
    ptext->setText("欢迎您使用远程协助,通过它您可以连接到别人的电脑帮助别人解决问题,或共享您的电脑让别人来解决您的问题");


    ptext->setWordWrap(true);
    ptext->setFixedSize(231, 40);
    ptext->setAlignment(Qt::AlignHCenter);
    ptext->setStyleSheet("font-size:10px;"
                         "color:#848484;"
                         );//"font-face:SourceHanSansCN-Normal;"
    mainLayout->addSpacing(137 - (64 + 50));
    mainLayout->addWidget(ptext, 0 , Qt::AlignCenter);

    QPushButton* button = nullptr;
    button = new QPushButton;
    button->setFixedSize(160, 36);

    button->setText(" 我要求助 ");
    button->setIcon(QIcon(getThemeImage("assistant_help.png")));


    mainLayout->addSpacing(198 - (40 + 23 + 64 + 50));
    mainLayout->addWidget(button, 0, Qt::AlignCenter);

    connect(button, SIGNAL(clicked()), this, SLOT(changeToSharePanel()));

    button = new QPushButton;
    button->setFixedSize(160,36);
    button->setText(" 帮助别人 ");
    button->setIcon(QIcon(getThemeImage("assistant_heart.png")));

    connect(button, SIGNAL(clicked()), this, SLOT(changeToAccessPanel()));

    mainLayout->addSpacing(244 - (198 + 36));
    mainLayout->addWidget(button, 0, Qt::AlignCenter);
    mainLayout->addStretch();
    this->setLayout(mainLayout);
    setWidget(mainWidget);

}

void MainPanel::emitPanelChanged(ViewPanel v)
{
    qDebug() <<"emitPanelChanged";
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
