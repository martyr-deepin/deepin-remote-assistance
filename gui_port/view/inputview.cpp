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
    m_tokenEdit->setFixedWidth(DCC::ModuleContentWidth);
    m_tokenEdit->setFixedHeight(70);

//    font.setWordSpacing( 20);
    m_tokenEdit->setFont(font);




    QObject::connect(m_tokenEdit, SIGNAL(returnPressed()), this, SLOT(connectToClient()));
    QObject::connect(m_tokenEdit, &QLineEdit::textChanged, [this](const QString& token){
        qDebug() << "valid token";
        QString copyToken = token;
        int pos = 0;
        m_connectButton->setEnabled(false);
        if (m_validator->validate(copyToken, pos) == QValidator::Acceptable) {
            m_connectButton->setEnabled(true);
            m_tip->setText(tr("Start remote access after clicking on \"Connect\""));
        } else if (m_tip->text() == tr("Start remote access after clicking on \"Connect\"")){
            m_tip->setText(tr("Please enter the verification code in the input field above"));
        }
    });



    QHBoxLayout *m_buttonHLayout = new QHBoxLayout;
    QPixmap pixmap(getThemeImage("blue_button_normal.png"));

    QPalette   pal;
    pal.setColor(QPalette::ButtonText, QColor(255,255,255));




    auto button = new DTextButton(tr("取消"));
    QObject::connect(button, &DTextButton::clicked, [this] (bool){
        emit cancel();
    });
    button->setMask(pixmap.mask());
    button->setStyleSheet("QPushButton{border-image:url(" + getThemeImage("blue_button_normal.png") + ");}"
                         "QPushButton:hover{border-image:url("+ getThemeImage("button_hover.png") + ");}"
                         "QPushButton:pressed{border-image:url(" + getThemeImage("button_press.png") +");}");
    button->setFixedSize(120, 32);
    button->setPalette(pal);

    m_connectButton->setFixedSize(120, 32);
    m_connectButton->setPalette(pal);
    m_connectButton->setStyleSheet("QPushButton{border-image:url(" + getThemeImage("blue_button_normal.png") + ");}"
                         "QPushButton:hover{border-image:url("+ getThemeImage("button_hover.png") + ");}"
                         "QPushButton:pressed{border-image:url(" + getThemeImage("button_press.png") +");}");



    m_buttonHLayout->addWidget(button);
    m_buttonHLayout->addWidget(m_connectButton);






    layout->addWidget(m_tokenEdit, 0, Qt::AlignHCenter);

//    auto separator = new QWidget;
//    separator->setObjectName("separator");
//    separator->setFixedSize(DCC::ModuleContentWidth-30, 1);
//    separator->setStyleSheet("background-color:red;");
//    layout->addWidget(separator);
//    layout->setAlignment(separator, Qt::AlignHCenter);

    m_tip = new QLabel;
    m_tip->setText(tr("请在上方输入验证码，完成“连接”后开始远程访问"));
    m_tip->setAlignment(Qt::AlignTop|Qt::AlignHCenter);
    m_tip->setFixedSize(300, 20);
    m_tip->setStyleSheet("font-size:10px;"
                         "color:#848484;"
                         );//"font-face:SourceHanSansCN-Normal;"



//    layout->addSpacing(10);
    layout->addWidget(m_tip, 0, Qt::AlignHCenter);
    layout->addLayout(m_buttonHLayout);
    mainWidget->setLayout(layout);
    setStyleSheet(readStyleSheet("inputview"));
    return mainWidget;
}

void InputView::focus() {
    qDebug() << "focus token input widget";
    m_tokenEdit->setFocus();
}
