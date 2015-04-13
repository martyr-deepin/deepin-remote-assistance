
import QtQuick 2.2
import QtQuick.Window 2.2
import QtQuick.Controls 1.1
import com.canonical.Oxide 1.0

Window {
    id: root
    width: 640
    height: 480

    // Emit this signal when fullscreen button clicked
    signal fullscreenToggled()

    // Emit cmd message signal
    signal cmdMessaged()

    property var starturl: Qt.resolvedUrl("http://peer.org:9000/remoting#client")
    property string remotingContext: 'remoting://'
    property string cmdMsg: 'cmd'
    property string keyboardMsg: 'keyboard'


    Column {
        anchors.fill: parent
        Row {
            id: navRow
            width: parent.width
            height: 24

            Button  {
                id: reloadButton
                height: parent.height
                text: "Reload"

                onClicked: {
                    webView.reload()
                }
            }

            Button {
                id: fullscreenButton
                height: parent.height
                text: 'Fullscreen'

                onClicked: {
                    root.fullscreenToggled()
                }
            }
        }

        WebView {
            id: webView
            width: parent.width
            height: parent.height - navRow.height
            url: starturl
            focus: true
            context: WebContext {
                cachePath: "file:///tmp/"
                dataPath: "file:///tmp/"
                devtoolsEnabled: true
                devtoolsPort: 9999
            }

            // Enable remote debug
            //property bool developerExtrasEnabled: true
            function sendMessage(msgId, msg) {
                rootFrame.sendMessage(remotingContext, msgId, {'detail': msg});
            }

            // Init message handlers
            Component.onCompleted: {
                rootFrame.addMessageHandler(cmdMsg, handleCmdMsg);
            }
        }

    }

    // Send messages to browser side
    function sendMessage(msgId, msg) {
        webView.sendMessage(msgId, msg);
    }

    // Handle cmd messages from browser
    ScriptMessageHandler {
        id: handleCmdMsg
        msgId: cmdMsg
        contexts: remotingContext
        callback: function (msg){
            console.log('TODO: emit cmd signal', msg);
        }
    }
}
