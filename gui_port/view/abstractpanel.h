/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#ifndef ABSTRACTPANEL_H
#define ABSTRACTPANEL_H

#include <QWidget>
#include <QFrame>
#include <QLayoutItem>
#include <QMouseEvent>

#include "../remoteassistance.h"

class QVBoxLayout;

class AbstractPanel : public QFrame
{
    Q_OBJECT
public:
    explicit AbstractPanel(const QString &title = QLatin1String(""), QWidget *parent = 0);
    AbstractPanel *addWidget(QWidget *);
    AbstractPanel *addLayout(QLayout *l, int stretch = 0);

protected slots:
    virtual void onNoNetwork();
    virtual void emitChangePanel();
    virtual void abort();

signals:
    void changePanel(ViewPanel);

protected:
    QVBoxLayout *m_viewLayout;
    QWidget *m_view;

    void setWidget(QWidget *);
};

#endif // ABSTRACTPANEL_H
