import QtQuick 2.2
import Deepin.Widgets 1.0

Rectangle {
    id: titlebar
    width: parent.width
    height: 30
    y: 0
    color: DConstants.bgColor

    readonly property string popdown: "popdown"
    readonly property string pullup: "pullup"
    state: popdown

    function showPreferencesMenu() {
        preferencesMenu.visible = true
    }

    DDragableArea {
        anchors.fill: parent
        window: windowView
        hoverEnabled: true
        onEntered: {
            // Popdown titlebar
            titlebar.state = popdown
            pullupTimer.stop()
        }
        onExited: {
            // Pullup titlebar
            pullupTimer.restart()
        }
        onDoubleClicked: {
            //windowView.toggleMaximized()
            toggleFullscreen()
        }
    }

    DssH2 {
        text: "Deepin Remote Assistance (Fullscreen Mode)"
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.verticalCenter: parent.verticalCenter
    }

    DTextButton {
        id: preferencesButton
        text: "Preferences \u25be"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        onClicked: {
            //showPreferencesMenu()
        }
    }

    /*
    DMenu {
        id: preferencesMenu
        posX: preferencesButton.x
        posY: preferencesButton.y + 20

        DMenuSeparator {
        }

        DToggleMenuItem {
            label: "FullScreen"
        }
    }
    */

    Row {
        anchors.right: parent.right
        height: parent.height
        
        //DTitleMinimizeButton {
        //    onClicked: {
        //            windowView.closeToSystemTray()
        //    }
        //}

        DTitleMaxUnmaxButton {
            // TODO: change image of button to unfullscreen
            maximized: true
            onClicked: {
                toggleFullscreen()
            }
        }

        DTitleCloseButton {
            onClicked: {
                windowView.close()
            }
        }
    }

    states: [
        State {
            name: popdown
            PropertyChanges {
                target: titlebar
                y: 0
            }
        },

        State {
            name: pullup
            PropertyChanges {
                target: titlebar
                y: -28
            }
        }
    ]

    Timer {
        id: pullupTimer
        interval: 2000
        running: titlebar.visible
        onTriggered: {
            titlebar.state = pullup
        }
    }

    transitions: [
        Transition {
            from: popdown
            to: pullup

            NumberAnimation {
                target: titlebar
                property: "y"
                duration: 300
            }
        },

        Transition {
            from: pullup
            to: popdown

            NumberAnimation {
                target: titlebar
                property: "y"
                duration: 80
            }
        }
    ]
}
