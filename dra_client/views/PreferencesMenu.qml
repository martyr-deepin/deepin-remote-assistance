
import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.2

import Deepin.Widgets 1.0

Menu {
    title: "Preferences"
    property alias fullscreenItem: fullscreenItem

    style: Component {
        MenuStyle {
            frame: Component {
                Item {
                    Rectangle {
                        anchors.fill: parent
                        color: "#151515"
                        antialiasing: true
                        //border.width: 2
                        //border.color: 'red'
                        //radius: 4
			            smooth: true
                    }
                }
            }
//                itemDelegate: Component {
//                }
            itemDelegate.background: Component {
                Rectangle {
                    color: styleData.selected ? "#252525" : "#151515"
                }
            }

            itemDelegate.label: Component {
                Text {
                    text: styleData.text
                    font.pixelSize: 12
                    color: styleData.selected ? "#01bdff" : "#b4b4b4"
                }
            }

            // Replace image indicator with text
            itemDelegate.checkmarkIndicator: Component {
                //Image {
                //    source: (styleData.checkable &&
                //             styleData.checked) ?  "checked.png" : ""
                //    }
                //}
                Text {
                    color: styleData.selected ? "#fafafa" : "#9a9a9a"
                    // check mark
                    //text: styleData.checked ? "\u2713" : ""
                    text: styleData.checked ? (styleData.exclusive ? "\u2022" : "\u2713") : ""
                    font.pixelSize: 12
                    y: -4
                }
            }
            //scrollIndicator:
            separator: Component {
                Item {
                    Rectangle {
                        anchors.centerIn: parent
                        color: "#212121"
                        height: 1
                        width: parent.width - 10
                        x: 1
                    }
                }
            }
            //submenuOverlap:
            //submenuPopupDelay:
        }
    }

    MenuItem { action: preferQuality }
    MenuItem { action: preferSpeed }
    MenuItem { action: balanced }

    MenuSeparator {}

    MenuItem {
        id: fullscreenItem
        text: "Fullscreen"
        checkable: true
        checked: root.state === "fullscreenMode"
        onToggled: {
            toggleFullscreen()
        }
    }

    ExclusiveGroup {
        id: videoQualityGroup

        Action {
            id: preferQuality
            text: "Optimize Quality"
            checkable: true
            onTriggered: {
                screenLevelChanged(screenLevelQuality)
            }
        }

        Action {
            id: preferSpeed
            text: "Optimize Speed"
            checkable: true
            onTriggered: {
                screenLevelChanged(screenLevelSpeed)
            }
        }

        Action {
            id: balanced
            text: "Balance"
            checkable: true
            // Default is `Balanced`
            checked: true
            onTriggered: {
                screenLevelChanged(screenLevelBalanced)
            }
        }
    }
}
