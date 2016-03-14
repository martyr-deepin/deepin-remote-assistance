#include "dmovie.h"

DMovie::DMovie(QObject *parent) : QObject(parent)
{
    connect(&m_timer,SIGNAL(timeout()), this, SLOT(play()));
    m_i = 0;
}

void  DMovie::start()
{
    m_timer.start(41.6);
}

void  DMovie::play()
{

switch(movieType) {
    case DMovie::list:
        if(m_i < m_imageListSize)
        {
//            qDebug() << "path:" + m_imageList.at(m_i);
            m_pixmap.load( m_path + m_imageList.at(m_i));
            m_label->setPixmap(m_pixmap);
            m_i++;
        }else{
            m_i = 0;
        }
        break;
    case DMovie::anifile:
        break;
}

}

void DMovie::setMoviePath(QString path, QLabel *label)
{
    m_path = path;
    QDir dir( path );
    dir.setFilter(QDir::Files| QDir::NoDotAndDotDot);
    QStringList list = dir.entryList();
//    qDebug() << list;
    movieType = DMovie::list;
    m_imageList = list;
//    qDebug() << m_imageList;
    m_imageListSize = list.size();
    m_label = label;
}

