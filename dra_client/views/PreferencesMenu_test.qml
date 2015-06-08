
import QtQuick 2.2
import QtQuick.Controls 1.2

import Deepin.Widgets 1.0

Rectangle {
    width: 480
    height: 320
    color: 'black'

    /*
    Button {
        id: showButton
        text: "Show"
        menu: preferencesMenu
    }
    */
   DTextButton {
       x: 5
       y: 5
       text: "Preferences \u25be"
        onClicked: {
            preferencesMenu.__popup(x, y + height + 2, 0)
            print(preferencesMenu.fullscreenItem.checked)
        }
   }

    PreferencesMenu {
        id: preferencesMenu
    }
}
