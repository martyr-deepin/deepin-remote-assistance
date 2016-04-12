#ifndef NOTIFYLABEL_H
#define NOTIFYLABEL_H

#include <QLabel>

class NotifyLabel : public QLabel
{
    Q_OBJECT

public:
    explicit NotifyLabel(QWidget *parent = 0);
    explicit NotifyLabel(QString text, QWidget *parent = 0);
    ~NotifyLabel() {}
};

#endif // NOTIFYLABEL_H
