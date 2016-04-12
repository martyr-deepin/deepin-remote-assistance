/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include "connectingview.h"

#include <QLabel>
#include <QVBoxLayout>

#include <dthememanager.h>
#include <dloadingindicator.h>
#include "widgets/simplebutton.h"
#include <QBitmap>

#include "constants.h"

#include "../helper.h"
#include "dmovie.h"

DWIDGET_USE_NAMESPACE

ConnectingView::ConnectingView(QWidget*p)
    : AbstractView(p)
{
    setObjectName("ConnectingView");
    initialize();


}

QWidget* ConnectingView::createMainWidget()
{
    auto mainWidget = new QWidget;

    auto mainLayout = new QVBoxLayout(mainWidget);
    mainLayout->setSpacing(0);
    mainLayout->setMargin(0);



//    auto loadingImage = new DLoadingIndicator(displayWidget);
//    loadingImage->setFixedSize(16, 16);
    
//    loadingImage->setImageSource(QPixmap(getThemeImage("waiting.png")));
//    loadingImage->setAniDuration(720);
//    loadingImage->setLoading(true);
//    displayLayout->addWidget(loadingImage);

    QLabel *movieLabel = new QLabel;
    movieLabel->setFixedSize(32,32);
    QString path = ":/dark/images/Spinner32/";
    DMovie *movie = new DMovie(movieLabel);
    movie->setMoviePath(path, movieLabel);

    movie->start();

    mainLayout->addWidget(movieLabel, 0, Qt::AlignCenter);
    mainLayout->addSpacing(20);

    auto label = new QLabel;
    label->setObjectName("msg");
    label->setText(tr("正在建立连接，请稍候......"));
    label->setAlignment(Qt::AlignVCenter);
    mainLayout->addWidget(label, 0, Qt::AlignCenter);


//    displayLayout->addStretch();
//    mainLayout->addWidget(displayWidget);

//    auto line = new QWidget;
//    line->setObjectName("separator");
//    line->setFixedHeight(1);
//    wrapLayout->addWidget(line);
//    wrapLayout->addSpacing(10);

//    auto waitingText = new QLabel;
//    waitingText->setObjectName("waitingText");
//    waitingText->setWordWrap(true);
//    waitingText->setAlignment(Qt::AlignTop|Qt::AlignHCenter);
//    waitingText->setText(tr("This panel will be hidden automatically and the remote session window will be opened on the desktop after connection is established successfully"));

//    wrapLayout->addWidget(waitingText);

    auto button = new SimpleButton(tr("取消"));
    connect(button, SIGNAL(clicked(bool)), this, SLOT(onCancelButtonClicked()));

    mainLayout->addWidget(button, 0, Qt::AlignCenter);

    return mainWidget;
}

void ConnectingView::onCancelButtonClicked()
{
    emit cancel();
}
