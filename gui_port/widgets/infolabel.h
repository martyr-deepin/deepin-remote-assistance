#ifndef INFOLABEL_H
#define INFOLABEL_H

#include <QLabel>

class InfoLabel : public QLabel
{
    Q_OBJECT

public:
    explicit InfoLabel(QWidget *parent = 0);
    explicit InfoLabel(QString text, QWidget *parent = 0);
    ~InfoLabel();
};

#endif // INFOLABEL_H
