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
#include "widgets/notifylabel.h"
#include "widgets/tiplabel.h"

DWIDGET_USE_NAMESPACE

ErrorView::ErrorView(QWidget* p)
    : AbstractView(p),
      m_text(new NotifyLabel(this))
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

    m_text->setFixedSize(DRA::NotifyLabelMaxWidth, DRA::NotifyLabelMaxHeight);
    m_text->setStyleSheet("NotifyLabel { font-size:20px; color: #ff8000; }");
    mainLayout->addSpacing(62);
    mainLayout->addWidget(m_text, 0, Qt::AlignHCenter);
    mainLayout->addSpacing(37);

    TipLabel *tip = new TipLabel(this);
    tip->setText(tr("Invalid verification code, please retry!"));
    tip->setFixedSize(DRA::TipLabelMaxWidth, DRA::TipLabelMaxHeight);
    mainLayout->addWidget(tip, 0, Qt::AlignHCenter);

    return mainWidget;
}

ErrorView* ErrorView::setText(const QString& text)
{
    m_text->setText(text);

    return this;
}
