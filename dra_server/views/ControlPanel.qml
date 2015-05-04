import QtQuick 2.2
import QtQuick.Controls 1.2
import Deepin.Widgets 1.0

DShadowRect {
    id: root
    defaultWidth: 280
    defaultHeight: 40

    //property bool showBlur: !(windowView.visibility === 4 || windowView.visibility === 5)
    property bool showBlur: true
    blurWidth: showBlur ? 10 : 0
    rectRadius: showBlur ? 3 : 0
    borderWidth: showBlur ? 1 : 0

    property var dconstants: DConstants{}

    // Disconnect button clicked
    signal disconnected()

    Rectangle {
        id: container
        width: parent.width
        height: parent.height
        color: dconstants.bgColor

        DDragableArea {
            anchors.fill: parent
            window: root
            //window: windowView
            onPressed: {
                print("title pressed...")
            }
            onReleased: {
                print("title released...")
            }
        }

        Button {
            id: disconnectBtn
            text: 'Disconnect'
            onClicked: {
                root.disconnected();
            }
        }
    }
}

