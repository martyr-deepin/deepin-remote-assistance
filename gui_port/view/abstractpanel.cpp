/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include <dbasebutton.h>

#include "abstractpanel.h"
#include "constants.h"
#include "errorview.h"

#include <QDebug>
#include <QVBoxLayout>

DWIDGET_USE_NAMESPACE

AbstractPanel::AbstractPanel(const QString& /*title*/, QWidget *parent)
    : QFrame(parent),
      m_viewLayout(new QVBoxLayout),
      m_view(new QWidget(this))
{
    m_viewLayout->setSpacing(0);
    m_viewLayout->setMargin(0);

    setLayout(m_viewLayout);

    setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Preferred);
    setFixedWidth(DRA::WindowContentWidth);
    setFixedHeight(DRA::WindowContentHeight);

    setObjectName("AbstractPanel");
}

void AbstractPanel::emitChangePanel()
{
    emit changePanel(ViewPanel::Main);
}

AbstractPanel *AbstractPanel::addWidget(QWidget *w)
{
    m_viewLayout->insertWidget(0, w, 0, Qt::AlignHCenter);
    return this;
}

AbstractPanel *AbstractPanel::addLayout(QLayout *l, int stretch)
{
    m_viewLayout->addLayout(l, stretch);
    return this;
}

void AbstractPanel::setWidget(QWidget *w)
{
    m_view->hide();
    m_view->deleteLater();
    m_view = w;
    addWidget(w);
}

void AbstractPanel::abort()
{
}

void AbstractPanel::onNoNetwork()
{
    qDebug() << "no network";
    auto view = new ErrorView;
    auto button = new DBaseButton(tr("Confirm"));
    button->setFixedSize(160,36);
    QObject::connect(button, &DBaseButton::clicked, [this] {
        abort();
    });
    view->addButton(button);

    setWidget(view->setText(tr("Network connection unavailable, please retry...")));
}


