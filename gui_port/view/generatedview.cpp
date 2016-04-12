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

#include "widgets/simplebutton.h"
#include "constants.h"
#include "../helper.h"
#include "widgets/tiplabel.h"

GeneratedView::GeneratedView(const QString& token, QWidget* p)
    : AbstractView(p),
      m_copyTipVisableTimer(new QTimer(this))
{
    setObjectName("GeneratedView");
    m_copyTipVisableTimer->setInterval(3000);
    QObject::connect(m_copyTipVisableTimer, &QTimer::timeout, [this] {
        m_copyTip->setText("");
    });

    initialize();

    QFont font("SourceHanSansCN-Light", 30);
    font.setLetterSpacing(QFont::AbsoluteSpacing, 10);
//    font.setWordSpacing( 20);
    m_token->setFont(font);
    m_token->setText(token);
}

QWidget* GeneratedView::createMainWidget()
{
    auto mainWidget = new QWidget;

    auto layout = new QVBoxLayout;
    layout->setSpacing(0);
    layout->setMargin(0);

    layout->addSpacing(78);

    m_token = new QLabel;
    m_token->setObjectName("token");

    layout->addWidget(m_token);
    layout->setAlignment(m_token, Qt::AlignCenter);
//    layout->addSpacing(40);

    QHBoxLayout *m_buttonHLayout = new QHBoxLayout;

    SimpleButton *button = new SimpleButton(tr("复制"),this);

    connect(button, &SimpleButton::clicked, [this] {
        m_copyTip->setText(tr("成功复制到剪贴板"));
        QString token = m_token->text();
        QApplication::clipboard()->setText(token);
        qDebug() << "Copy Code button on GeneratedView is clicked.";
        m_copyTipVisableTimer->stop();
        m_copyTipVisableTimer->start();
    });

    m_buttonHLayout->addWidget(button);

    SimpleButton *buttonn = new SimpleButton(tr("取消"));

    connect(buttonn, &SimpleButton::clicked, [this] {
        qDebug() << "cancel button on GeneratedView is clicked";
        emit cancel();
    });

    m_buttonHLayout->addWidget(buttonn);

    m_copyTip = new QLabel;
    m_copyTip->setObjectName("copyTip");
    m_copyTip->setText(tr("成功复制到剪贴板"));
    m_copyTip->setAlignment(Qt::AlignHCenter);
    m_copyTip->setFixedWidth(DRA::ModuleContentWidth);
    m_copyTip->setStyleSheet("font-size:10px;"
                         "color:#848484;"
                         ); //not support "font-face:SourceHanSansCN-Normal;"

    m_copyTip->setText("");

    auto tip = new TipLabel(this);
    tip->setText(tr("如需共享您的桌面，请将上面的验证码提供给协助您的人"));
    tip->setFixedSize(DRA::TipLabelMaxWidth, DRA::TipLabelMaxHeight);

    layout->addSpacing(20);
    layout->addWidget(tip,0,Qt::AlignCenter);
    layout->addSpacing(20);
    layout->addWidget(m_copyTip);
    layout->addSpacing(10);
    layout->addLayout(m_buttonHLayout);
    layout->addStretch();

    mainWidget->setLayout(layout);
    return mainWidget;
}
