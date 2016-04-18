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
#include "widgets/infolabel.h"

DWIDGET_USE_NAMESPACE

GeneratingView::GeneratingView(QWidget* p)
    : AbstractView(p)
{
    setObjectName("GeneratingView");
    initialize();
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

    InfoLabel* text = new InfoLabel;
    text->setText(tr("Generating verification code, please wait... "));

    auto mainLayout = new QVBoxLayout(mainWidget);
    mainLayout->setSpacing(0);
    mainLayout->setMargin(0);

    mainLayout->addSpacing(60);
    mainLayout->addWidget(label, 0, Qt::AlignHCenter);
    mainLayout->addSpacing(30);
    mainLayout->addWidget(text, 0, Qt::AlignHCenter);

    addButton(button);

    return mainWidget;
}
