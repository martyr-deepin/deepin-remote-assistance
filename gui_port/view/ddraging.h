#ifndef DDRAGING_H
#define DDRAGING_H

#include <QObject>
#include <QWidget>
#include <QFrame>
#include <QMouseEvent>
#include <QDebug>
#include <QTimer>






class DDraging : public QFrame
{
public:
    DDraging(QFrame *parent = 0 );


protected:
    void mousePressEvent(QMouseEvent *event);
    void mouseReleaseEvent(QMouseEvent *event);
    void mouseMoveEvent(QMouseEvent * event );

private:

    bool shouldMove;
    QPoint formerMainPos;
    QPoint formerMousePos;

};

#endif // DDRAGING_H
