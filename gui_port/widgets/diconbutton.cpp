#include "diconbutton.h"

#include <QDebug>
#include <QStyle>
#include <QMouseEvent>
#include <QEvent>

#include <dthememanager.h>

DIconButton::DIconButton(QWidget *parent)
    : QPushButton(parent)
{
//    D_THEME_INIT_WIDGET(DIconButton);
    changeState();
}

DIconButton::DIconButton(const QString &normalPic, const QString &hoverPic, const QString &pressPic, QWidget *parent)
    : QPushButton(parent)
{
//    D_THEME_INIT_WIDGET(DIconButton);

    if (!normalPic.isEmpty())
        m_normalPic = normalPic;
    if (!hoverPic.isEmpty())
        m_hoverPic = hoverPic;
    if (!pressPic.isEmpty())
        m_pressPic = pressPic;

    setCheckable(false);

    changeState();
}

DIconButton::DIconButton(const QString &normalPic, const QString &hoverPic,
                           const QString &pressPic, const QString &checkedPic, QWidget *parent)
    : QPushButton(parent)
{
//    D_THEME_INIT_WIDGET(DIconButton);

    if (!normalPic.isEmpty())
        m_normalPic = normalPic;
    if (!hoverPic.isEmpty())
        m_hoverPic = hoverPic;
    if (!pressPic.isEmpty())
        m_pressPic = pressPic;
    if (!checkedPic.isEmpty())
        m_checkedPic = checkedPic;

    setCheckable(true);

    changeState();
}

DIconButton::~DIconButton()
{
}

void DIconButton::enterEvent(QEvent *event)
{
    setCursor(Qt::PointingHandCursor);

    if (!m_isChecked){
        m_state = Hover;
        changeState();
    }

    event->accept();
    //QLabel::enterEvent(event);
}

void DIconButton::leaveEvent(QEvent *event)
{
    if (!m_isChecked){
        m_state = Normal;
        changeState();
    }

    event->accept();
    //QLabel::leaveEvent(event);
}

void DIconButton::mousePressEvent(QMouseEvent *event)
{
    m_state = Press;
    changeState();

    event->accept();
    //QLabel::mousePressEvent(event);
}

void DIconButton::mouseReleaseEvent(QMouseEvent *event)
{
    m_state = Hover;
    changeState();

    emit clicked();

    if (m_isCheckable){
        m_isChecked = !m_isChecked;
        if (m_isChecked){
            m_state = Checked;
        } else {
            m_state = Normal;
        }
        changeState();
    }

    event->accept();
    //QLabel::mouseReleaseEvent(event);
}

void DIconButton::changeState()
{
    switch (m_state) {
    case Hover:     if (!m_hoverPic.isEmpty()) setIcon(QPixmap(m_hoverPic));      break;
    case Press:     if (!m_pressPic.isEmpty()) setIcon(QPixmap(m_pressPic));      break;
    case Checked:   if (!m_checkedPic.isEmpty()) setIcon(QPixmap(m_checkedPic));  break;
    default:        if (!m_normalPic.isEmpty()) setIcon(QPixmap(m_normalPic));    break;
    }

    emit stateChanged();
}

void DIconButton::setCheckable(bool flag)
{
    m_isCheckable = flag;

    if (!m_isCheckable){
        m_state = Normal;
        changeState();
    }
}

void DIconButton::setChecked(bool flag)
{
    if (m_isCheckable == false){
        return;
    }

    m_isChecked = flag;
    if (m_isChecked){
        m_state = Checked;
    } else {
        m_state = Normal;
    }
    changeState();
}

bool DIconButton::isChecked()
{
    return m_isChecked;
}

bool DIconButton::isCheckable()
{
    return m_isCheckable;
}

void DIconButton::setNormalPic(const QString &normalPicPixmap)
{
    m_normalPic = normalPicPixmap;
    changeState();
}

void DIconButton::setHoverPic(const QString &hoverPicPixmap)
{
    m_hoverPic = hoverPicPixmap;
    changeState();
}

void DIconButton::setPressPic(const QString &pressPicPixmap)
{
    m_pressPic = pressPicPixmap;
    changeState();
}

void DIconButton::setCheckedPic(const QString &checkedPicPixmap)
{
    m_checkedPic = checkedPicPixmap;
    changeState();
}

DIconButton::State DIconButton::getState() const
{
    return m_state;
}
