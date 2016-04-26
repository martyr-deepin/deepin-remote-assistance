#ifndef DICONBUTTON_H
#define DICONBUTTON_H

#include <dbasebutton.h>

class DIconButton : public QPushButton
{
    Q_OBJECT
    Q_PROPERTY(QString normalPic READ getNormalPic WRITE setNormalPic DESIGNABLE true)
    Q_PROPERTY(QString hoverPic READ getHoverPic WRITE setHoverPic DESIGNABLE true)
    Q_PROPERTY(QString pressPic READ getPressPic WRITE setPressPic DESIGNABLE true)
    Q_PROPERTY(QString checkedPic READ getCheckedPic WRITE setCheckedPic DESIGNABLE true)

public:
    DIconButton(QWidget * parent=0);

    DIconButton(const QString & normalPic, const QString & hoverPic,
                 const QString & pressPic, QWidget *parent = 0);

    DIconButton(const QString & normalPic, const QString & hoverPic,
                 const QString & pressPic, const QString & checkedPic, QWidget * parent = 0);

    ~DIconButton();

    void setChecked(bool flag);
    void setCheckable(bool flag);
    bool isChecked();
    bool isCheckable();

    void setNormalPic(const QString & normalPic);
    void setHoverPic(const QString & hoverPic);
    void setPressPic(const QString & pressPic);
    void setCheckedPic(const QString & checkedPic);

    inline const QString getNormalPic() const {return m_normalPic;}
    inline const QString getHoverPic() const {return m_hoverPic;}
    inline const QString getPressPic() const {return m_pressPic;}
    inline const QString getCheckedPic() const {return m_checkedPic;}

    enum State {Normal, Hover, Press, Checked};

    State getState() const;

signals:
    void clicked();
    void stateChanged();

protected:
    void enterEvent(QEvent * event);
    void leaveEvent(QEvent * event);
    void mousePressEvent(QMouseEvent * event);
    void mouseReleaseEvent(QMouseEvent * event);

private:
    void changeState();

private:

    State m_state = Normal;

    bool m_isChecked = false;
    bool m_isCheckable = false;
    QString m_normalPic;
    QString m_hoverPic;
    QString m_pressPic;
    QString m_checkedPic;
};


#endif // DICONBUTTON_H
