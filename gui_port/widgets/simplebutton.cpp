#include "simplebutton.h"

#include "../helper.h"

SimpleButton::SimpleButton(QString text, QWidget *parent) :
    QPushButton(text, parent)
{
    setStyleSheet("QPushButton{color: white}"
                  "QPushButton{border-image:url(" + getThemeImage("blue_button_normal.png") + ");}"
                  "QPushButton:hover{border-image:url("+ getThemeImage("button_hover.png") + ");}"
                  "QPushButton:pressed{border-image:url(" + getThemeImage("button_press.png") +");}");
    setFixedSize(120, 32);
}

SimpleButton::~SimpleButton()
{

}
