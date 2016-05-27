#include "aboutdialog.h"

#include <QVBoxLayout>
#include <QLabel>
#include <QIcon>
#include <QEvent>


DAboutDialog::DAboutDialog(Dtk::Widget::DWindow *parent) : Dtk::Widget::DWindow(parent)
{
    setTitle(tr("Remote Assistance"));
    setWindowIcon(QIcon(":/Resource/remote-assistance-48.png"));
    setBackgroundColor(qRgb(0xf5, 0xf5, 0xf8));

    setWindowFlags(windowFlags() & ~ Qt::WindowMinimizeButtonHint);
    setWindowFlags(windowFlags() & ~ Qt::WindowSystemMenuHint);
    setWindowFlags(windowFlags() & ~ Qt::WindowMaximizeButtonHint);

    QLabel *logo = new QLabel("logo");
    logo->setPixmap(QPixmap(":/Resource/remote-assistance-96.png"));
    logo->setFixedSize(96, 96);

    QLabel *productName = new QLabel(tr("Deepin Remote Assistance"));
    productName->setStyleSheet("font-size:18px;");

    QLabel *version = new QLabel(tr("Version: 2.0"));
    version->setStyleSheet("font-size:12px; color: #666666");

    QPixmap companyLogoPixmap(":/Resource/logo.png");
    QLabel *companyLogo = new QLabel("companyLogo");
    companyLogo->setPixmap(companyLogoPixmap);
    companyLogo->setFixedSize(companyLogoPixmap.size());

    QLabel *website = new QLabel();
    website->setStyleSheet("font-size:13px; color: #004EE5");
    website->setOpenExternalLinks(false);
    website->setText("<a href='www.deepin.org' style='text-decoration: none;'>www.deepin.org</a>");
    connect(website, SIGNAL(linkActivated(QString)),
            this, SLOT(onLogLinkActivated(QString)));

    QString textFormat = "<p style='text-indent: 24px;'>%1</p>";
    QString descriptionText =  textFormat.arg(tr("Remote Assistance is a remote controller, users can connect to computers between each other with it."));
    QLabel *description = new QLabel(descriptionText);
    description->setStyleSheet("font-size:12px; color: #1A1A1A; border: 0px solid;");
    description->setWordWrap(true);
    description->adjustSize();
    description->setFixedWidth(400 - 38 * 2);

    QVBoxLayout *mainLayout = new QVBoxLayout;
    mainLayout->addWidget(logo);
    mainLayout->setAlignment(logo, Qt::AlignCenter);
    mainLayout->addSpacing(8);
    mainLayout->addWidget(productName);
    mainLayout->setAlignment(productName, Qt::AlignCenter);
    mainLayout->addSpacing(12);
    mainLayout->addWidget(version);
    mainLayout->setAlignment(version, Qt::AlignCenter);
    mainLayout->addSpacing(12);
    mainLayout->addWidget(companyLogo);
    mainLayout->setAlignment(companyLogo, Qt::AlignCenter);
    mainLayout->addSpacing(2);
    mainLayout->addWidget(website);
    mainLayout->setAlignment(website, Qt::AlignCenter);
    mainLayout->addSpacing(26);
    mainLayout->addWidget(description);
    mainLayout->setAlignment(description, Qt::AlignCenter);
    mainLayout->addSpacing(26);
    mainLayout->addStretch();

    setLayout(mainLayout);

    this->adjustSize();
//    this->setFixedSize(this->size());
}

bool DAboutDialog::event(QEvent *event)
{
    switch (event->type()) {
    case QEvent::ActivationChange:
        if (!this->isActiveWindow()) {
            this->close();
        }
        break;
    default:
        break;
    }
    return Dtk::Widget::DWindow::event(event);
}

void DAboutDialog::focusOutEvent(QFocusEvent * /*event*/)
{
    // hide();
}

#include <QDesktopServices>
#include <QUrl>
#include <QDebug>

void DAboutDialog::onLogLinkActivated(const QString &link)
{
    qDebug() << this->size();
    if (link == "www.deepin.org") {
        QDesktopServices::openUrl(QUrl(link));
    }
}
