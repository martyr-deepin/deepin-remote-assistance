
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

    property var starturl: Qt.resolvedUrl("http://peer.org:9000/remoting#client")

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

            // Enable remote debug
            property bool developerExtrasEnabled: true

            context: WebContext {
                devtoolsEnabled: true
                devtoolsPort: 9999
            }
        }

        /*
        Label {
            id: statusLabel
            text: webView.loading ?
                    "Loading" + " (%1%)".arg(webView.loadProgress) :
                    "Page loaded"
            width: parent.width
        }
        */
    }

// This signal is handled in Python
//    onActiveChanged: {
//        console.log(active);
//    }
}
