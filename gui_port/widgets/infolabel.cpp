#include "infolabel.h"

InfoLabel::InfoLabel(QWidget *parent) :
    QLabel(parent)
{
    setStyleSheet("TipLabel { font-size:12px; color:#000000; }");
    setWordWrap(true);
    setAlignment(Qt::AlignHCenter | Qt::AlignTop);

    setFixedSize(200,16);

    setObjectName("InfoLabel");
//    setStyleSheet("InfoLabel { border: 1px solid black } ");
}

InfoLabel::InfoLabel(QString text, QWidget *parent) :
    InfoLabel(parent)
{
    setText(text);
}

InfoLabel::~InfoLabel()
{

}
