/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#ifndef REMOTE_ASSISTANCE_H
#define REMOTE_ASSISTANCE_H

#include <QObject>
#include <QWidget>
#include <QScopedPointer>
#include <libdui_global.h>
#include "dbus/manager.h"
#include "view/ddraging.h"

QT_BEGIN_NAMESPACE
class QFrame;
QT_END_NAMESPACE

DWIDGET_BEGIN_NAMESPACE
class DStackWidget;
class DWindow;
DWIDGET_END_NAMESPACE

class RemoteAssistance;

enum ViewPanel
{
    Main,
    Share,
    Access,
};

class Impl : public QObject
{
    Q_OBJECT
public:
    Impl(RemoteAssistance *, com::deepin::daemon::Remoting::Manager *);
    ~Impl();
    inline void popView(QWidget *w = nullptr, bool isDelete = true, int count = 1, bool enableTransition = true);
    inline void pushView(QWidget *w, bool enableTransition = true);
    void initPanel();
    void changePanel(ViewPanel);
    void changeTitle(ViewPanel v);

public:
    QWidget *getPanel(ViewPanel);

    RemoteAssistance *m_pub;
    com::deepin::daemon::Remoting::Manager *m_manager;
    DTK_NAMESPACE::Widget::DWindow *m_view; // NB: the m_view will be reparented, should not delete it in dtor.
    DTK_NAMESPACE::Widget::DStackWidget *m_stackWidget; // this is child of m_view.
    QWidget *m_panel;
    ViewPanel m_viewType;

    QWidget* m_mainPanel;
    QWidget* m_accessPanel;
    QWidget* m_sharePanel;
};


class RemoteAssistance: public QObject
{
    Q_OBJECT
public:
    RemoteAssistance();
    ~RemoteAssistance();

    void showWindow();

public slots:
    void changePanel(ViewPanel);

private:
    QScopedPointer<Impl> m_impl;

private slots:
    void onAnimationEnd();
    void hide();
protected:
    void mousePressEvent (QMouseEvent *event)
       {
           qDebug() <<"adsf";
       }



};

#endif /* end of include guard: REMOTE_ASSISTANCE_H */
