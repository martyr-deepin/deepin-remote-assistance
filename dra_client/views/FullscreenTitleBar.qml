import QtQuick 2.2
import QtQml 2.2

import Deepin.Widgets 1.0

Rectangle {
    id: titlebar
    width: parent.width
    y: 0
    color: "#1a1b1b"

    readonly property int defaultHeight: 30

    // When cursor move to top of screen, push down title bar
    readonly property int grabCursorY: 1

    height: defaultHeight

    readonly property string popdown: "popdown"
    readonly property string pullup: "pullup"
    state: pullup

    DDragableArea {
        anchors.fill: parent
        window: windowView
        onDoubleClicked: {
            //toggleFullscreen()
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
        
//        DTitleMinimizeButton {
//            onClicked: {
//                    toggleFullscreen()
//                    windowView.closeToSystemTray()
//            }
//        }
//
//        DTitleMaxUnmaxButton {
//            // TODO: change image of button to unfullscreen
//            //maximized: true
//            onClicked: {
//                toggleFullscreen()
//            }
//        }
//
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
                if (root.cursorY <= grabCursorY) {
                    if (state != popdown) {
                        state = popdown
                    }
                    pullupTimer.restart()
                } else if (root.cursorY <= defaultHeight && state === popdown) {
                    pullupTimer.restart()
                } else if (preferencesMenu.visible) {
                    pullupTimer.restart()
                }
                // FIXME: do not pullup titlebar when preferencesMenu is visible
            }
        }
    }

    Timer {
        id: pullupTimer
        interval: 1500
        running: titlebar.visible
        onTriggered: {
            titlebar.state = pullup
        }
    }

}
