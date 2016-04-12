#ifndef TIPLABEL_H
#define TIPLABEL_H

#include <QLabel>

class TipLabel : public QLabel
{
    Q_OBJECT

public:
    explicit TipLabel(QWidget *parent = 0);
    explicit TipLabel(QString text, QWidget *parent = 0);
    ~TipLabel();
};

#endif // TIPLABEL_H
