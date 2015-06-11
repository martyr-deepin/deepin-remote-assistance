import QtQuick 2.2
import Deepin.Widgets 1.0

Rectangle {
    width: parent.width
    height: 30
    color: DConstants.bgColor

    DDragableArea {
        anchors.fill: parent
        window: windowView
        onPressed: {
        }
        onReleased: {
        }
        onDoubleClicked: {
            //windowView.toggleMaximized()
        }
    }

    DssH2 {
        text: dsTr("Deepin Remote Assistance")
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.verticalCenter: parent.verticalCenter
    }

    DTextButton {
        id: preferencesButton
        text: dsTr("Preferences") + " \u25be"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        onClicked: {
            preferencesMenu.__popup(0, height, 0)
        }

        Binding {
            target: preferencesMenu
            property: "__visualItem"
            value: preferencesButton
        }
    }

    Row {
        anchors.right: parent.right
        height: parent.height
        
        DTitleMinimizeButton {
            onClicked: {
                windowView.closeToSystemTray()
            }
        }

        DTitleMaxUnmaxButton {
            Binding on maximized {
                value: windowView.visibility === 4
            }
            onClicked: {
                windowView.toggleMaximized()
            }
        }

        DTitleCloseButton {
            onClicked: {
                windowView.close()
            }
        }
    }
}
