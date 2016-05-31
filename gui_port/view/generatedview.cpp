/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include "generatedview.h"

#include <QApplication>
#include <QClipboard>
#include <QLabel>
#include <QVBoxLayout>
#include <QTimer>
#include <QDebug>
#include <QFont>
#include <QPixmap>
#include <QBitmap>

#include <dbasebutton.h>
#include "constants.h"
#include "../helper.h"

DWIDGET_USE_NAMESPACE

GeneratedView::GeneratedView(const QString &token, QWidget *p)
    : AbstractView(p),
      m_copyTipVisableTimer(new QTimer(this))
{
    setObjectName("GeneratedView");
    m_copyTipVisableTimer->setInterval(3000);
    QObject::connect(m_copyTipVisableTimer, &QTimer::timeout, [this] {
        m_tokenLabel->show();
        m_copyTip->hide();
//        m_tipLabel->setText(tr("To share your desktop, please provide the above verification code to your help provider"));
    });

    initialize();

    m_tokenLabel->setText(token);
    m_token = token;
}

QWidget *GeneratedView::createMainWidget()
{
    auto mainWidget = new QWidget;

    auto layout = new QVBoxLayout(mainWidget);
    layout->setSpacing(0);
    layout->setMargin(0);

    layout->addSpacing(70);

    m_copyTip = new QLabel;
    m_copyTip->setFixedHeight(32);
    m_copyTip->setText(tr("Copied to clipboard successfully"));
    m_copyTip->setStyleSheet("font-size: 20px;");
    m_copyTip->hide();

    m_tokenLabel = new NotifyLabel(this);
    m_tokenLabel->setObjectName("token");
    m_tokenLabel->setFixedWidth(200);
    m_tokenLabel->setTextInteractionFlags(Qt::TextSelectableByMouse);

    QFont font = m_tokenLabel->font();
    font.setPixelSize(30);
    font.setLetterSpacing(QFont::AbsoluteSpacing, 16);

    m_tokenLabel->setStyleSheet("margin-left: 4px;");
    m_tokenLabel->setFont(font);
    m_tokenLabel->setAlignment(Qt::AlignCenter);

    layout->addWidget(m_copyTip, 0, Qt::AlignCenter);
    layout->addWidget(m_tokenLabel, 0, Qt::AlignCenter);

    DBaseButton *copyBt = new DBaseButton(tr("Copy"), this);
    copyBt->setFixedSize(160, 36);

    connect(copyBt, &DBaseButton::clicked, [this] {
        m_tokenLabel->hide();
        m_copyTip->show();
//        m_tipLabel->setText(tr("Connecting, please wait..\ninterface will close after successfully connected"));
        QString token = m_tokenLabel->text();
        QApplication::clipboard()->setText(m_token);
        qDebug() << "Copy Code button on GeneratedView is clicked.";
        m_copyTipVisableTimer->stop();
        m_copyTipVisableTimer->start();
    });
    addButton(copyBt);

    /*
    DBaseButton *cancelBt = new DBaseButton(tr("Cancel"));
    cancelBt->setFixedSize(160, 36);

    connect(cancelBt, &DBaseButton::clicked, [this] {
        qDebug() << "cancel button on GeneratedView is clicked";
        emit cancel();
    });
    addButton(cancelBt);
    */

    m_tipLabel = new TipLabel(this);
    m_tipLabel->setText(tr("To share your desktop, please provide the above verification code to your help provider"));
    m_tipLabel->setFixedSize(DRA::TipLabelMaxWidth, DRA::TipLabelMaxHeight);

    layout->addSpacing(36);
    layout->addWidget(m_tipLabel, 0, Qt::AlignHCenter);
    layout->addSpacing(20);
    layout->addSpacing(18);
    layout->addStretch();

    return mainWidget;
}
