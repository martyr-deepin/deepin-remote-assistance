#ifndef SIMPLEBUTTON_H
#define SIMPLEBUTTON_H

#include <QObject>
#include <QPushButton>

class SimpleButton : public QPushButton
{
    Q_OBJECT

public:
    explicit SimpleButton(QString text, QWidget *parent = 0);
    ~SimpleButton();
};

#endif // SIMPLEBUTTON_H
