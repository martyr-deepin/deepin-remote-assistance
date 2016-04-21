#pragma once

#include <DWindow>
#include <QDebug>

class DAboutDialog : public Dtk::Widget::DWindow
{
    Q_OBJECT
public:
    DAboutDialog(Dtk::Widget::DWindow *parent);


signals:

protected:
    bool event(QEvent * event);
    void focusOutEvent(QFocusEvent* event);

public slots:
    void onLogLinkActivated(const QString &link);
};

