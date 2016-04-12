/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include "errorview.h"

#include <QDebug>
#include <QLabel>
#include <QVBoxLayout>

#include <dthememanager.h>

#include "constants.h"
#include "../helper.h"

DWIDGET_USE_NAMESPACE

ErrorView::ErrorView(QWidget* p)
    : AbstractView(p),
      m_text(new QLabel)
{
    setObjectName("ErrorView");
    initialize();
}

QWidget* ErrorView::createMainWidget()
{
     auto mainWidget = new QWidget;
     auto mainLayout = new QVBoxLayout(mainWidget);
     mainLayout->setSpacing(0);
     mainLayout->setMargin(0);

    m_text->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
//    m_text->setFixedSize(DRA::ModuleContentWidth, 70);
//    m_text->setAlignment(Qt::AlignCenter);
    m_text->setWordWrap(true);
    m_text->setStyleSheet(" font-size : 20px; color:#ff8000; ");

    mainLayout->addWidget(m_text, 0, Qt::AlignCenter);

    QLabel * msgBox = new QLabel;
    msgBox->setText("您输入的验证码无效，请重新输入");
    msgBox->setStyleSheet("font-size:10px;"
                          "color:#848484;");
//    mainLayout->addSpacing(10);
    mainLayout->addWidget(msgBox, 0, Qt::AlignCenter);

    setStyleSheet(readStyleSheet("errorview"));
    return mainWidget;
}

ErrorView* ErrorView::setText(const QString& text)
{
    m_text->setText(text);

    return this;
}
