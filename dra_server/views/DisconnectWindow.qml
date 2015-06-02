/****************************************************************************
**
**  Copyright (C) 2011~2014 Deepin, Inc.
**                2011~2014 WanQing Yang
**
**  Author:     WanQing Yang <match.yangwanqing@gmail.com>
**  Maintainer: WanQing Yang <match.yangwanqing@gmail.com>
**
**  This program is free software: you can redistribute it and/or modify
**  it under the terms of the GNU General Public License as published by
**  the Free Software Foundation, either version 3 of the License, or
**  any later version.
**
**  This program is distributed in the hope that it will be useful,
**  but WITHOUT ANY WARRANTY; without even the implied warranty of
**  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**  GNU General Public License for more details.
**
**  You should have received a copy of the GNU General Public License
**  along with this program.  If not, see <http://www.gnu.org/licenses/>.
**
****************************************************************************/

import QtQuick 2.2
import QtQuick.Window 2.2
import QtGraphicalEffects 1.0

import DBus.Com.Deepin.Daemon.Display 1.0
import Deepin.Widgets 1.0

Rectangle {
    id: root
    color: "transparent"

    Component.onCompleted: {
        windowView.setX(screenSize.width - width - 100)
        windowView.setY(screenSize.y + shadowWidth)
    }

    width: window.width
    height: 30 + window.shadowRadius * 2

    // Disconnect button clicked
    signal disconnected()

    property int shadowWidth: 0

    // Display main dialog
    function showDialog(){
        windowView.show()
        windowView.raise()
    }

    function hideDialog(){
        windowView.hide()
    }

    property var displayId: Display {}

    property var screenSize: QtObject {
        property int x: displayId.primaryRect[0]
        property int y: displayId.primaryRect[1]
        property int width: displayId.primaryRect[2]
        property int height: displayId.primaryRect[3]
    }

    property var dconstants: QtObject {
        property string textNormalColor: '#fafafa'
        property string textHoverColor: '#9a9a9a'
    }

    Rectangle {
        id: window
        anchors.centerIn: parent
        width: contentText.contentWidth + 40
        height: parent.height
        radius: 5
        color: "transparent"

        property int shadowRadius: 3
        property real shadowAlpha: 0.5

        RectangularGlow {
            id: effect
            anchors.fill: rootFrame
            glowRadius: window.shadowRadius
            spread: 0.2
            color: Qt.rgba(0, 0, 0, window.shadowAlpha)
            cornerRadius: window.radius + glowRadius
        }

        Rectangle{
            id: rootFrame
            width: parent.width - window.shadowRadius * 2
            height: parent.height - window.shadowRadius * 2
            anchors.centerIn: parent
            radius: window.radius

            color: Qt.rgba(0, 0, 0, 0.85)
            border.color: Qt.rgba(1, 1, 1, 0.2)
            border.width: 1
        }

        DDragableArea{
            anchors.fill: parent
            window: windowView
        }

        Image {
            id: grabImg
            source: "images/grab.png"
            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 6 + window.shadowRadius
            }
        }

        Text {
            id: contentText
            anchors {
                right: parent.right
                rightMargin: 6 + window.shadowRadius
                //verticalCenter: parent.verticalCenter
                top: parent.top
                bottom: parent.bottom
            }
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            text: "Disconnect"
            color: dconstants.textNormalColor

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onEntered:contentText.color = dconstants.textHoverColor
                onExited: contentText.color = dconstants.textNormalColor
                onClicked: {
                    // Show confirmation dialog
                    root.disconnected()
                }
            }
        }
    }
}
