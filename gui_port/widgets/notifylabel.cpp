#include "notifylabel.h"

NotifyLabel::NotifyLabel(QWidget *parent) :
    QLabel(parent)
{
    setWordWrap(true);
    setAlignment(Qt::AlignHCenter);
    setStyleSheet("NotifyLabel { font-size:20px; color:black; }");
}

NotifyLabel::NotifyLabel(QString text, QWidget *parent) :
    NotifyLabel(parent)
{
    setText(text);
}
