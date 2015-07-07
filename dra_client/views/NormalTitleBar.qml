import QtQuick 2.2
import Deepin.Widgets 1.0

Rectangle {
    width: parent.width
    height: 30
    color: "#1a1b1b"

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
            // Popup preferences menu at bottom of this button
            windowView.popupPreferencesMenu(x + 14, y + height + 14)
        }
    }

    Row {
        anchors.right: parent.right
        height: parent.height
        
        DTitleMinimizeButton {
            onClicked: {
                windowView.visibility = 3
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
