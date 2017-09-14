/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#ifndef ACCESS_PANEL_H_T7BZFECR
#define ACCESS_PANEL_H_T7BZFECR

#include <QString>

#include "abstractpanel.h"
#include "../controller/access.h"

class IAccessController;
class InputView;

class AccessPanel: public AbstractPanel
{
    Q_OBJECT
public:
    AccessPanel(IAccessController *controller, QWidget *p = nullptr);
    ~AccessPanel();

signals:
    void connected();

public slots:
    void focus();

private slots:
    void onStopped();
    void onConnect(QString);
    void onConnecting();
    void onConnected();
    void onConnectFailed(AccessErrors);
    void onDisconnected();
    void onCancel();
    void abort() Q_DECL_OVERRIDE;

private slots:
    void emitChangePanel() Q_DECL_OVERRIDE;

private:
    IAccessController   *m_controller;
};

#endif /* end of include guard: ACCESS_PANEL_H_T7BZFECR */
