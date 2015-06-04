import QtQuick 2.2
import Deepin.Widgets 1.0

DShadowRect {
    id: root
    defaultWidth: 998
    defaultHeight: 593

    property bool showBlur: !(windowView.visibility === 4 || windowView.visibility === 5)
    blurWidth: showBlur ? 10 : 0
    rectRadius: showBlur ? 3 : 0
    borderWidth: showBlur ? 1 : 0

    // Emit window closed signal when close button is clicked
    signal windowClosed()

    // Emit this signal when fullscreen button clicked
    //signal fullscreenToggled()

    // Set width and height property of media stream
    function setVideoAspectRatio(width, height) {
        screenVideoRect.aspectRatio = width / height
    }

    // Toggle window status between maximized and normal
    function toggleWindowStatus() {
        if(windowView.visibility != 4){
            windowView.visibility = 4
        }
        else{
            windowView.visibility = 2
        }
    }

    // Size of web view
    // These properties are read in messaging module
    // Cursor position relative to web view
    property int cursorX: 0
    property int cursorY: 0
    property bool captureCursor: false

    function getCaptureCursor() {
        return captureCursor;
    }

    function getCursorX() {
        // TODO: use parseInt()
        //return cursorX + parseInt(screenVideoRect.webView.x);
        return cursorX + screenVideoRect.webView.x;
    }

    function getCursorY() {
        return cursorY + screenVideoRect.webView.y;
    }

    function getVideoWidth () {
        return screenVideoRect.webView.width;
    }

    function getVideoHeight() {
        return screenVideoRect.webView.height;
    }

    Rectangle {
        id: titleBar
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
                toggleWindowStatus()
            }
        }

        DssH2 {
            text: "Deepin Remote Assistance"
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
        }

        Row {
            anchors.right: parent.right
            height: parent.height
            
            DTitleMinimizeButton {
                onClicked: {
                    //windowView.visibility = 3
                    windowView.closeToSystemTray()
                }
            }
            DTitleMaxUnmaxButton {
                Binding on maximized {
                    value: windowView.visibility === 4
                }
                onClicked: {
                    toggleWindowStatus()
                }
            }
            DTitleCloseButton {
                onClicked: {
                    windowView.close()
                    root.windowClosed()
                }
            }
        }
    }

    // web frame
    ScreenVideoRect {
        id: screenVideoRect
        anchors.top: titleBar.bottom
        width: parent.width
        height: parent.height - titleBar.height

        //onEntered: {
            //print("entered:", x, y)
        //}
        //onExited: {
            //print("exited:", x, y)
        //}
        //onCursorPositionChanged: {
            //print(x, y)
        //}
    }
}

