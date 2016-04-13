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


    m_token->setText(token);

}

QWidget* GeneratedView::createMainWidget()
{
    auto mainWidget = new QWidget;

    auto layout = new QVBoxLayout(mainWidget);
    layout->setSpacing(0);
    layout->setMargin(0);

    layout->addSpacing(70);

    m_token = new NotifyLabel(this);
    m_token->setObjectName("token");
    m_token->setFixedSize(200, 36);
    QFont font = m_token->font();
    font.setPixelSize(30);
    m_token->setFont(font);

    qDebug() << font.pixelSize() << "------------------------";


//    m_token->setStyleSheet("background-color:red");
//    qDebug() << m_token->styleSheet();
//    m_token->setStyleSheet("NotifyLabel { font-size:20px; color: red; }");
//    m_token->setStyleSheet(m_token->styleSheet());
//    m_token->setStyleSheet("NotifyLabel { font-size: 30px; color:black; }");

    layout->addWidget(m_token, 0, Qt::AlignHCenter);


    SimpleButton *button = new SimpleButton(tr("复制"),this);

    connect(button, &SimpleButton::clicked, [this] {
        m_copyTip->setText(tr("成功复制到剪贴板"));
        QString token = m_token->text();
        QApplication::clipboard()->setText(token);
        qDebug() << "Copy Code button on GeneratedView is clicked.";
        m_copyTipVisableTimer->stop();
        m_copyTipVisableTimer->start();
    });

    SimpleButton *buttonn = new SimpleButton(tr("取消"));

    connect(buttonn, &SimpleButton::clicked, [this] {
        qDebug() << "cancel button on GeneratedView is clicked";
        emit cancel();
    });


    addButton(button);
    addButton(buttonn);



    m_copyTip = new QLabel;
    m_copyTip->setObjectName("copyTip");
    m_copyTip->setText(tr("成功复制到剪贴板"));
    m_copyTip->setAlignment(Qt::AlignHCenter);
    m_copyTip->setFixedWidth(DRA::ModuleContentWidth);
//    m_copyTip->setStyleSheet("font-size:24px;"
//                         "color:#848484;");

    m_copyTip->setText("");

    auto tip = new TipLabel(this);
    tip->setText(tr("如需共享您的桌面，请将上面的验证码提供给协助您的人"));
    tip->setFixedSize(DRA::TipLabelMaxWidth, DRA::TipLabelMaxHeight);

    layout->addSpacing(35.6);
    layout->addWidget(tip,0,Qt::AlignHCenter);
    layout->addSpacing(20);
    layout->addWidget(m_copyTip);
    layout->addSpacing(18);
    layout->addStretch();

    return mainWidget;
}
