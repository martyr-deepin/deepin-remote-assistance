/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#ifndef SHARE_PANEL_H_WNAMLTE2
#define SHARE_PANEL_H_WNAMLTE2

#include <QString>
#include "abstractpanel.h"

class IShareController;
class QLabel;
class AbstractView;

class SharePanel : public AbstractPanel
{
    Q_OBJECT
public:
    SharePanel(IShareController *, QWidget *p = nullptr);
    ~SharePanel();

public slots:
    void onGeneratingAccessToken();
    void onGenAccessTokenFailed();
    void onGenAccessTokenSuccessed(QString);
    void onDisconnectedWithAsk();
    void onDisconnected();
    void onSharing();
    void onStop();
    void onRetry();

private slots:
    void emitChangePanel() Q_DECL_OVERRIDE;
    void abort() Q_DECL_OVERRIDE;

private:
    void dtor();

private:
    QTimer              *m_deleyRetryTimer;
    IShareController    *m_controller;
};

#endif /* end of include guard: SHARE_PANEL_H_WNAMLTE2 */
