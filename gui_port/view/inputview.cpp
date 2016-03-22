/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#include "inputview.h"

#include <QLabel>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QTimer>
#include <QRegExp>
#include <QRegExpValidator>
#include <QDebug>
#include <QBitmap>

#include <dthememanager.h>
#include <dtextbutton.h>

#include "constants.h"

#include "../helper.h"

DWIDGET_USE_NAMESPACE

InputView::InputView(QWidget* p)
    : AbstractView(p),
      m_validator(new QRegExpValidator(*new QRegExp("[A-Za-z0-9]{6}"), this)),
      m_connectButton(new DTextButton(tr("连接")))
{
    setObjectName("InputView");
    m_connectButton->setEnabled(false);
    QObject::connect(m_connectButton, &DTextButton::clicked, this, &InputView::emitConnect);

    initialize();

    focus();

}

void InputView::emitConnect()
{
    emit connect(m_tokenEdit->text().trimmed());
}

void InputView::connectToClient()
{
    if (m_connectButton->isEnabled()) {
        emitConnect();
    }
}

QWidget* InputView::createMainWidget()
{
    auto mainWidget = new QWidget;
    auto layout = new QVBoxLayout;
    layout->setSpacing(0);
    layout->setMargin(0);
    QFont font("SourceHanSansCN-Light", 30);
    font.setLetterSpacing(QFont::AbsoluteSpacing, 10);

    m_tokenEdit = new QLineEdit;
    m_tokenEdit->setMaxLength(6);
    m_tokenEdit->setAttribute(Qt::WA_TranslucentBackground);
    m_tokenEdit->setAlignment(Qt::AlignCenter);
    m_tokenEdit->setFixedWidth(DRA::ModuleContentWidth);
    m_tokenEdit->setFixedHeight(70);

//    font.setWordSpacing( 20);
    m_tokenEdit->setFont(font);


    QPixmap pixmap(getThemeImage("blue_button_normal.png"));

    QPalette   pal;
    pal.setColor(QPalette::ButtonText, QColor(255,255,255));




    m_cancelButton = new DTextButton(tr("取消"));
    QObject::connect(m_cancelButton, &DTextButton::clicked, [this] (bool){
        emit cancel();
    });
    m_cancelButton->setMask(pixmap.mask());
    m_cancelButton->setStyleSheet("QPushButton{border-image:url(" + getThemeImage("blue_button_normal.png") + ");}"
                         "QPushButton:hover{border-image:url("+ getThemeImage("button_hover.png") + ");}"
                         "QPushButton:pressed{border-image:url(" + getThemeImage("button_press.png") +");}");
    m_cancelButton->setFixedSize(120, 32);
    m_cancelButton->setPalette(pal);

    m_connectButton->setFixedSize(120, 32);
    m_connectButton->setPalette(pal);
    m_connectButton->setStyleSheet("QPushButton{border-image:url(" + getThemeImage("blue_button_normal.png") + ");}"
                         "QPushButton:hover{border-image:url("+ getThemeImage("button_hover.png") + ");}"
                         "QPushButton:pressed{border-image:url(" + getThemeImage("button_press.png") +");}");
    m_connectButton->hide();



    QObject::connect(m_tokenEdit, SIGNAL(returnPressed()), this, SLOT(connectToClient()));
    QObject::connect(m_tokenEdit, &QLineEdit::textChanged, [this](const QString& token){
        qDebug() << "valid token";
        QString copyToken = token;
        int pos = 0;
        m_connectButton->setEnabled(false);
        m_connectButton->hide();
        m_cancelButton->show();
        if (m_validator->validate(copyToken, pos) == QValidator::Acceptable) {
            m_connectButton->setEnabled(true);
            m_connectButton->show();
            m_cancelButton->hide();
//            m_tip->setText(tr("Start remote access after clicking on \"Connect\""));
//        } else if (m_tip->text() == tr("Start remote access after clicking on \"Connect\"")){
//            m_tip->setText(tr("Please enter the verification code in the input field above"));
        }
    });



    QHBoxLayout *m_buttonHLayout = new QHBoxLayout;




    m_buttonHLayout->addWidget(m_cancelButton);
    m_buttonHLayout->addWidget(m_connectButton);
//    m_connectButton->hide();





    layout->addSpacing(56);
    layout->addWidget(m_tokenEdit, 0, Qt::AlignCenter);



    m_tip = new QLabel;
    m_tip->setText(tr("请在上方输入验证码，完成“连接”后开始远程访问"));
    m_tip->setAlignment(Qt::AlignTop|Qt::AlignCenter);
    m_tip->setFixedSize(300, 20);
    m_tip->setStyleSheet("font-size:10px;"
                         "color:#848484;"
                         );//"font-face:SourceHanSansCN-Normal;"



    layout->addSpacing(10);
    layout->addWidget(m_tip, 0, Qt::AlignCenter);
    layout->addSpacing(40);
    layout->addLayout(m_buttonHLayout);
    layout->addStretch();
    mainWidget->setLayout(layout);
    setStyleSheet(readStyleSheet("inputview"));
    return mainWidget;
}

void InputView::focus() {
    qDebug() << "focus token input widget";
    m_tokenEdit->setFocus();
}