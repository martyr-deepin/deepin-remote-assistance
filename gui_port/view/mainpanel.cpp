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
#include <libdui/dseparatorhorizontal.h>
#include <QPushButton>

#include "constants.h"
#include "moduleheader.h"

#include "mainpanel.h"
#include "buttongroup.h"
#include "button.h"
#include "helper.h"

DUI_USE_NAMESPACE

MainPanel::MainPanel(com::deepin::daemon::Remoting::Manager* manager, QWidget*p): AbstractPanel(tr(" "), p), m_buttongroup(new ButtonGroup)
{
    setObjectName("MainPanel");
    m_manager = manager;

    // addWidget(new DSeparatorHorizontal);
    // m_buttongroup->setGroupTitle(tr("Remote Assistance"));


    setWindowTitle("远程协助");

    QLabel *picon = new QLabel(this);
    picon->setPixmap(QPixmap(getThemeImage("icon.png")));
    picon->resize(64,64);
    picon->move((360-64)/2, 50);
    picon->show();

    QLabel *ptext = new QLabel(this);
    ptext->setText("欢迎您使用远程协助,通过它您可以连接到别人的电脑帮助别人解决问题,或共享您的电脑让别人来解决您的问题");
  //  ptext->move((360-236)/2,50+88 );
//    ptext->adjustSize();
    ptext->setGeometry(QRect((360-236)/2,50+88, 236, 64));
    ptext->setWordWrap(true);
    ptext->setAlignment(Qt::AlignHCenter);
    ptext->setStyleSheet("font-size:10px;"
                         "color:#848484;"
                         "font-face:SourceHanSansCN-Normal;");

    QPushButton* button = nullptr;
    button = new QPushButton(this);
    button->resize(160,36);
    button->move(100, 200);
    button->setText(" 我要求助 ");
    button->setIcon(QIcon(getThemeImage("assistant_help.png")));

    connect(button, SIGNAL(clicked()), this, SLOT(changeToSharePanel()));

    button = new QPushButton(this);
    button->resize(160,36);
    button->move(100, 246);
    button->setText(" 帮助别人 ");
    button->setIcon(QIcon(getThemeImage("assistant_heart.png")));

    connect(button, SIGNAL(clicked()), this, SLOT(changeToAccessPanel()));

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
