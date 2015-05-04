import QtQuick 2.2
import QtGraphicalEffects 1.0

Item {
    property int defaultWidth: 400
    property int defaultHeight: 300
    width: defaultWidth + sideWidth * 2;
    height: defaultHeight + sideWidth * 2
    property color blurColor: Qt.rgba(0, 0, 0, 0.3)
    property color borderColor: Qt.rgba(255, 255, 255, 0.33)
	property color blackBorderColor: Qt.rgba(30/255.0, 30/255.0, 30/255.0, 0.6)
	property real blurWidth: 10
	property real rectRadius: 5
    property int borderWidth: 1
	property real sideWidth: blurWidth + rectRadius
	property rect vaildRect: Qt.rect(sideWidth, sideWidth, width - sideWidth * 2, height - sideWidth * 2)
    property bool visibleBackgroundImage: true
    property alias backgoundColor: rect.color

    default property alias content: container.children
	
    RectangularGlow {
        id: effect
        anchors.fill: rect
        glowRadius: blurWidth
        spread: 0.2
        color: blurColor
        cornerRadius: rect.radius + glowRadius
    }
	
    Rectangle {
        id: rect
		x: sideWidth; y: sideWidth
        width: Math.round(parent.width - sideWidth * 2 )
        height: Math.round(parent.height - sideWidth * 2)
        radius: rectRadius		
		anchors.centerIn: parent		
		antialiasing: true
		color: "transparent"
		smooth: true
		
		
		Rectangle {
			id: backgound
			anchors.fill: parent
			color: "transparent"
			antialiasing: true
			smooth: true
			
			Image {
				anchors.fill: parent
				//source: "qrc:/images/common/bg.png"
                visible: visibleBackgroundImage
			}
			
			/* Rectangle { */
			/* 	anchors.fill: parent */
			/* 	color: Qt.rgba(0.9, 0.9, 0.9, 0.2) */
			/* } */
			
			Rectangle {
                id: blackBorder
				border { width: borderWidth; color: blackBorderColor }
				anchors.fill: parent
				color: "transparent"
				radius: rectRadius
			}
			
            Rectangle {
                id: container
                anchors.margins: blackBorder.border.width
                anchors.fill: parent
                color: "transparent"
                radius: rectRadius
            }
		}
		
		//RoundItem {
			//target: backgound
			//radius: rectRadius
		//}

    }
}
