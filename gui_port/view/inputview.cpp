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

#include "widgets/simplebutton.h"
#include "widgets/tiplabel.h"

#include "constants.h"
#include "../helper.h"

static const QString TokenLineEditStyle = "QLineEdit#TokenLineEdit { "
                                          "background: white; "
                                          "border: 1px solid rgba(0, 0, 0, 0.1); "
                                          "border-radius: 4px; "
                                          "}";

InputView::InputView(QWidget* p)
    : AbstractView(p),
      m_validator(new QRegExpValidator(*new QRegExp("[A-Za-z0-9]{6}"), this)),
      m_connectButton(new SimpleButton(tr("Cancel")))
{
    setObjectName("InputView");
    m_buttonFlag = InputView::btncancel;

    QObject::connect(m_connectButton, &SimpleButton::clicked, [this]{
        switch(m_buttonFlag)
        {
            case InputView::btncancel:
                emit cancel();
                break;
            case InputView::btnconnect:
                emitConnect();
                break;
        }

    });


    initialize();

    focus();
}

void InputView::emitConnect()
{
    emit connect(m_tokenEdit->text().trimmed());
}

void InputView::connectToClient()
{
    if (InputView::btnconnect == m_buttonFlag) {
        emitConnect();
    }
}

QWidget* InputView::createMainWidget()
{
    auto mainWidget = new QWidget;
    auto layout = new QVBoxLayout;
    layout->setSpacing(0);
    layout->setMargin(0);

    m_tokenEdit = new QLineEdit;
    m_tokenEdit->setMaxLength(6);

    m_tokenEdit->setAlignment(Qt::AlignCenter);
    m_tokenEdit->setFixedWidth(DRA::ModuleContentWidth);
    m_tokenEdit->setFixedHeight(70);

    // Set style for our token edit box.
    m_tokenEdit->setObjectName("TokenLineEdit");
    m_tokenEdit->setStyleSheet(TokenLineEditStyle);

    QFont font = m_tokenEdit->font();
    font.setPixelSize(30);
    m_tokenEdit->setFont(font);


    QObject::connect(m_tokenEdit, SIGNAL(returnPressed()), this, SLOT(connectToClient()));
    QObject::connect(m_tokenEdit, &QLineEdit::textChanged, [this](const QString& token){
        qDebug() << "valid token";
        QString copyToken = token;
        int pos = 0;

        m_connectButton->setText(tr("Cancel"));
        m_buttonFlag = InputView::btncancel;
        if (m_validator->validate(copyToken, pos) == QValidator::Acceptable) {
            m_connectButton->setText(tr("Connect"));
            m_buttonFlag = InputView::btnconnect;
        }
    });

    QHBoxLayout *m_buttonHLayout = new QHBoxLayout;

    addButton(m_connectButton);

    layout->addSpacing(56);
    layout->addWidget(m_tokenEdit, 0, Qt::AlignCenter);

    m_tip = new TipLabel(this);
    m_tip->setText(tr("Input verification code and \"Connect\" to start remote access"));
    m_tip->setFixedSize(DRA::TipLabelMaxWidth, DRA::TipLabelMaxHeight);

    layout->addSpacing(20);
    layout->addWidget(m_tip, 0, Qt::AlignCenter);
    layout->addSpacing(40);
//    layout->addLayout(m_buttonHLayout);
    layout->addStretch();
    mainWidget->setLayout(layout);
    return mainWidget;
}

void InputView::focus() {
    qDebug() << "focus token input widget";
    m_tokenEdit->setFocus();
}
