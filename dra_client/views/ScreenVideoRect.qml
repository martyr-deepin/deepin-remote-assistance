import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 1.1
import QtQuick.Dialogs 1.1

import com.canonical.Oxide 1.0

Rectangle {
    id: webViewRoot
    width: 1000
    height: 600

    // URL of deepin peer server
    property var startUrl: Qt.resolvedUrl('http://10.0.0.42:9000/remoting#client')
    // Msg URI, schema://path/object
    property string remotingContext: 'remoting://'

    // To mark cmd message
    property string cmdMsg: 'CMD'

    // To mark keyboard message
    property string keyboardMsg: 'KEYBOARD'

    // To mark mouse message
    property string mouseMsg: 'MOUSE'

    // Default width of video
    property int screenVideoWidth: 800

    // Default height of video
    property int screenVideoHeight: 600

    // Video aspect ratio
    property real aspectRatio: screenVideoWidth / screenVideoHeight

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

        userScripts: [
            // This script is used to setup message channel between QML and 
            // web frame
            UserScript {
                context: remotingContext
                matchAllFrames: true
                url: Qt.resolvedUrl("oxide-user.js")
            }
        ]
    }

    // Handle cmd messages from browser
    ScriptMessageHandler {
        id: handleCmdMsg
        msgId: cmdMsg
        contexts: remotingContext
        callback: function (msg){
            console.log('emit cmd signal', msg.args.detail);
            root.cmdMessaged(msg.args.detail);
        }
    }

    WebView {
        id: webView
        anchors.centerIn: parent
        width: Math.min(parent.width, parent.height * aspectRatio)
        height: Math.min(parent.height, Math.round(parent.width / aspectRatio))

        url: startUrl
        focus: true
        context: webContext

        function sendMessage(msgId, msg) {
            console.log('will send message to browser:', msgId, msg);
            rootFrame.sendMessage(remotingContext, msgId, {'detail': msg});
        }

        // Init message handlers
        Component.onCompleted: {
            rootFrame.addMessageHandler(handleCmdMsg);
        }

        // This mouse area is used to mark mouse position in web frame
        // Its relative position will be sent to remote peer
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true

            onEntered: {
                root.captureCursor = true
            }

            onExited: {
                root.captureCursor = false
            }

            onPositionChanged: {
                root.cursorX = mouse.x
                root.cursorY = mouse.y
                //webViewRoot.cursorPositionChanged(
                    //webView.width, webView.height, mouseX, mouseY)
            }
        }
    }
}
