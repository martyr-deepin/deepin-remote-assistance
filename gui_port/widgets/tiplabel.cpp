#include "tiplabel.h"

TipLabel::TipLabel(QWidget *parent) :
    QLabel(parent)
{
    setStyleSheet("TipLabel { font-size:10px; color:#848484; }");
    setWordWrap(true);
    setAlignment(Qt::AlignHCenter | Qt::AlignTop);
}

TipLabel::TipLabel(QString text, QWidget *parent) :
    TipLabel(parent)
{
    setText(text);
}

TipLabel::~TipLabel()
{

}
