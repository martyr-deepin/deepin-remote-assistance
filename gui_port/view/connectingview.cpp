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
#include <dbasebutton.h>
#include <QBitmap>

#include "constants.h"

#include "../helper.h"
#include "dmovie.h"

#include <dspinbox.h>

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

    // TODO: refactory to make this block one linear
    QLabel *movieLabel = new QLabel;
    movieLabel->setFixedSize(32,32);

    // FIXME: hidpi
    QString path = ":/resource/theme/images/spinner/32/";
    DMovie *movie = new DMovie(movieLabel);
    movie->setMoviePath(path, movieLabel);
    movie->start();

    mainLayout->addSpacing(70);
    mainLayout->addWidget(movieLabel, 0, Qt::AlignCenter);
    mainLayout->addSpacing(20);

    auto label = new QLabel;
    label->setObjectName("msg");
    label->setText(tr("Establishing connection, please wait..."));
    label->setAlignment(Qt::AlignVCenter);
    mainLayout->addWidget(label, 0, Qt::AlignCenter);

    auto button = new DBaseButton(tr("Cancel"));
    button->setFixedSize(160,36);
    connect(button, SIGNAL(clicked(bool)), this, SLOT(onCancelButtonClicked()));

    addButton(button);

    return mainWidget;
}

void ConnectingView::onCancelButtonClicked()
{
    emit cancel();
}
