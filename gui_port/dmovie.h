#ifndef DMOVIE_H
#define DMOVIE_H

#include <QObject>
#include <QTimer>
#include <QLabel>
#include <QPixmap>
#include <QStringList>
#include <QDebug>
#include <QFile>
#include <QDir>
#include <QApplication>



class DMovie : public QObject
{
    Q_OBJECT
public:

    explicit DMovie(QObject *p = 0);
    void setMoviePath(QString path, QLabel *label);

    enum{
        notype,
        anifile,
        list
    }movieType;

signals:

public slots:
    void start();
    void play();


private:
    QStringList m_imageList;
    QString m_path;

    QLabel *m_label;
    int m_i;
    int m_imageListSize;
    QPixmap m_pixmap;
    QString m_aniFilePath;
    int m_picCount;
    int m_tmpCount;
    QFile m_anifile;
    QTimer m_timer;

};

#endif // DMOVIE_H
