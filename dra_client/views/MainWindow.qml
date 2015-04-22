import QtQuick 2.1
import Deepin.Widgets 1.0

DShadowRect {
    id: root
    defaultWidth: 998
    defaultHeight: 593

    property bool showBlur: !(windowView.visibility === 4 || windowView.visibility === 5)
    blurWidth: showBlur ? 10 : 0
    rectRadius: showBlur ? 3 : 0
    borderWidth: showBlur ? 1 : 0

    property var dconstants: DConstants{}

    // Emit cmd message signal
    signal cmdMessaged(string msg)

    // Emit window closed signal when close button is clicked
    signal windowClosed()

    // Emit this signal when fullscreen button clicked
    //signal fullscreenToggled()

    // Send messages to browser side
    function sendMessage(msgId, msg) {
        screenVideoRect.webView.sendMessage(msgId, msg);
    }

    // Set width and height property of video
    property alias screenVideoWidth: screenVideoRect.screenVideoWidth
    property alias screenVideoHeight: screenVideoRect.screenVideoHeight

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
        return cursorX;
    }

    function getCursorY() {
        return cursorY;
    }

    function getVideoWidth () {
        return screenVideoRect.webView.width;
    }

    function getVideoHeight() {
        return screenVideoRect.webView.height;
    }

    Rectangle{
        id: titleBar
        width: parent.width
        height: 30
        color: dconstants.bgColor

        DDragableArea{
            anchors.fill: parent
            window: windowView
            onPressed: {
                print("title pressed...")
            }
            onReleased: {
                print("title released...")
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
            
            DTitleOptionButton{
                // TODO: remove fullscreen mode
                onClicked:{
                    screenVideoRect.webView.fullscreen = !screenVideoRect.webView.fullscreen
                }
            }
            DTitleMinimizeButton{
                onClicked: {
                    windowView.visibility = 3
                }
            }
            DTitleMaxUnmaxButton{
                Binding on maximized {
                    value: windowView.visibility === 4
                }
                onClicked: {
                    if(windowView.visibility != 4){
                        windowView.visibility = 4
                    }
                    else{
                        windowView.visibility = 2
                    }
                }
            }
            DTitleCloseButton{
                onClicked: {
                    // Close main window and emit window-close signal
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
        screenVideoWidth: 1366
        screenVideoHeight: 768
        //starturl: "http://localhost/screen/"

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

