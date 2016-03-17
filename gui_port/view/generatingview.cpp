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
#include <dtextbutton.h>
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

    QPixmap pixmap(getThemeImage("blue_button_normal.png"));
    QPalette   pal;
    pal.setColor(QPalette::ButtonText, QColor(255,255,255));

    QPushButton *button = new QPushButton(tr("Cancel"),this);
    button->setMask(pixmap.mask());
    button->setStyleSheet("QPushButton{border-image:url(" + getThemeImage("blue_button_normal.png") + ");}"
                         "QPushButton:hover{border-image:url("+ getThemeImage("button_hover.png") + ");}"
                         "QPushButton:pressed{border-image:url(" + getThemeImage("button_press.png") +");}");
    button->setFixedSize(120, 32);
    button->setPalette(pal);
    connect(button, SIGNAL(clicked(bool)), this, SLOT(onCancelButtonClicked()));

    QWidget* mainWidget = new QWidget;

    mainWidget->setFixedSize(360, 320);

    auto mainLayout = new QVBoxLayout;
    mainLayout->setSpacing(0);
    mainLayout->setMargin(0);

    QLabel* text = new QLabel;
    text->setWordWrap(true);
    text->setAlignment(Qt::AlignVCenter);
    text->setText(tr("正在生成验证码，请稍候......"));

    mainLayout->addStretch();
    mainLayout->addWidget(label);
    mainLayout->setAlignment(label, Qt::AlignHCenter);
    mainLayout->addSpacing(24);
    mainLayout->addWidget(text);
    mainLayout->setAlignment(text, Qt::AlignHCenter);
    mainLayout->addSpacing(70);
    mainLayout->addWidget(button);
    mainLayout->setAlignment(button, Qt::AlignCenter);
    mainLayout->addSpacing(40);

    mainWidget->setLayout(mainLayout);

    return mainWidget;
}
