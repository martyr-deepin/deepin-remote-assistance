/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include "generatingview.h"

#include <QHBoxLayout>
#include <QLabel>
#include <QDebug>
#include <QThread>
#include <QBitmap>

#include <dthememanager.h>
#include <dseparatorhorizontal.h>
#include "widgets/simplebutton.h"
#include <dloadingindicator.h>

#include "constants.h"
#include "dmovie.h"
#include "../helper.h"

DWIDGET_USE_NAMESPACE

GeneratingView::GeneratingView(QWidget* p)
    : AbstractView(p)
{
    setObjectName("GeneratingView");
    initialize();



//    setStyleSheet(readStyleSheet("generatingview"));
}

void GeneratingView::onCancelButtonClicked()
{
    emit cancel();
}

QWidget* GeneratingView::createMainWidget()
{

    QLabel *label = new QLabel;
    label->setFixedSize(32,32);
    QString path = ":/dark/images/Spinner32/";
    DMovie *movie = new DMovie(label);
    movie->setMoviePath(path, label);
    movie->start();

    SimpleButton *button = new SimpleButton(tr("Cancel"),this);
    connect(button, SIGNAL(clicked(bool)), this, SLOT(onCancelButtonClicked()));

    QWidget* mainWidget = new QWidget;

    mainWidget->setFixedSize(360, 290);

    auto mainLayout = new QVBoxLayout;
    mainLayout->setSpacing(0);
    mainLayout->setMargin(0);

    QLabel* text = new QLabel;
    text->setWordWrap(true);
    text->setAlignment(Qt::AlignVCenter);
    text->setText(tr("正在生成验证码，请稍候......"));

    mainLayout->addSpacing(10);
    mainLayout->addWidget(label);
    mainLayout->setAlignment(label, Qt::AlignCenter);
    mainLayout->addWidget(text);
    mainLayout->setAlignment(text, Qt::AlignCenter);
    mainLayout->addWidget(button);
    mainLayout->setAlignment(button, Qt::AlignCenter);
    mainLayout->addSpacing(48);

    mainWidget->setLayout(mainLayout);

    return mainWidget;
}
