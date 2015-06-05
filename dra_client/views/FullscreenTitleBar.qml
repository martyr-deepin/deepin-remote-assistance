import QtQuick 2.2
import Deepin.Widgets 1.0

Rectangle {
    id: titlebar
    width: parent.width
    y: 0
    color: DConstants.bgColor

    readonly property int defaultHeight: 30
    height: defaultHeight

    readonly property string popdown: "popdown"
    readonly property string pullup: "pullup"
    state: pullup

    function showPreferencesMenu() {
        preferencesMenu.visible = true
    }

    DDragableArea {
        anchors.fill: parent
        window: windowView
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
                y: 0 - defaultHeight
            }
        }
    ]

    transitions: [
        Transition {
            from: popdown
            to: pullup

            NumberAnimation {
                target: titlebar
                property: "y"
                duration: 200
            }
        },

        Transition {
            from: pullup
            to: popdown

            NumberAnimation {
                target: titlebar
                property: "y"
                duration: 200
            }
        }
    ]

    Connections {
        target: eventHandler
        onCursorPositionChanged: {
            if (visible) {
                if (root.cursorY <= defaultHeight) {
                    pullupTimer.restart()
                    state = popdown
                } else {
                    pullupTimer.stop()
                    state = pullup
                }
            }
        }
    }

    Timer {
        id: pullupTimer
        interval: 1000
        running: titlebar.visible
        onTriggered: {
            titlebar.state = pullup
        }
    }

}
