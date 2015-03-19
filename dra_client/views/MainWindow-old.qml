
import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 1.1
import com.canonical.Oxide 1.0

Window {
    width: 1000
    height: 600

    //property var starturl: Qt.resolvedUrl("./index.html")
    property var starturl: Qt.resolvedUrl("http://peer.org:9000/screen#client")

    function updateWebView() {
        webView.url = locationField.text
    }

    Column {
        anchors.fill: parent
        Row {
            id: navRow
            width: parent.width
            height: locationField.height
            Button  {
                id: backButton
                height: locationField.height
                text: "后退"

                onClicked: {
                    webView.goBack()
                }
            }

            Button  {
                id: forwardButton
                height: locationField.height
                text: "前进"

                onClicked: {
                    webView.goForward()
                }
            }

            TextField {
                id: locationField
                width: parent.width - backButton.width - forwardButton.width
                text: starturl

                onAccepted: {
                    updateWebView()
                }
            }
        }

        WebView {
            id: webView
            width: parent.width
            height: parent.height - navRow.height - statusLabel.height
            url: starturl
            focus: true

            onUrlChanged: {
                locationField.text = url
            }
        }

        Label {
            id: statusLabel
            text: webView.loading ?
                    "Loading" + " (%1%)".arg(webView.loadProgress) :
                    "Page loaded"
            width: parent.width
        }
    }
}

