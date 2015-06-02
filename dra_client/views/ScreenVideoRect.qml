import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.1

import com.canonical.Oxide 1.0

Rectangle {
    id: webViewRoot
    width: 1000
    height: 800

    // URL of deepin peer server
    property var startUrl: Qt.resolvedUrl('http://10.0.0.42:9000/remoting#client')

    // Remote media stream aspect ratio
    property real aspectRatio: 1

    property alias webView: webView

    // Cursor moves on webView
    // Returns (webViewWidth, webViewHiehgt, offsetX, offsetY)
    // TODO: remove these signals
    signal cursorPositionChanged(int width, int height, int x, int y)

    // Cursor moves into webView
    signal cursorEntered(int x, int y)

    // Cursor leaves webView
    signal cursorLeaved(int x, int y)


    WebContext {
        id: webContext
        cachePath: 'file:///tmp/dra'
        dataPath: 'file:///tmp/dra'
        devtoolsEnabled: true
        devtoolsPort: 9999
    }

    WebView {
        id: webView
        anchors.centerIn: parent
        width: Math.min(parent.width, parent.height * aspectRatio)
        height: Math.min(parent.height, Math.round(parent.width / aspectRatio))

        url: startUrl
        focus: true
        context: webContext

        // This mouse area is used to mark mouse position in web frame
        // Its relative position will be sent to remote peer
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true

            // Hide cursor
            cursorShape: Qt.BlankCursor

            onEntered: {
                root.captureCursor = true
            }

            onExited: {
                root.captureCursor = false
            }

            onPositionChanged: {
                root.cursorX = mouse.x - webView.x;
                root.cursorY = mouse.y - webView.y;
            }
        }
    }
}
