import QtQuick 2.2

import Deepin.Locale 1.0
import Deepin.Widgets 1.0

DShadowRect {
    id: root
    defaultWidth: 998
    defaultHeight: 593

    state: "normalMode"

    property bool showBlur: !(windowView.visibility === 4 || windowView.visibility === 5)
    blurWidth: showBlur ? 10 : 0
    rectRadius: showBlur ? 3 : 0
    borderWidth: showBlur ? 1 : 0

    // Cursor position changed
    signal cursorMoved

    function toggleFullscreen() {
        windowView.toggleFullscreen()
        if (windowView.isFullscreen()) {
            state = "fullscreenMode"
        } else {
            state = "normalMode"
        }
    }

    // Changle screen quality
    signal screenLevelChanged(int level)

    readonly property int screenLevelSpeed: 0
    readonly property int screenLevelBalanced: 1
    readonly property int screenLevelQuality: 2

    // Set width and height property of media stream
    function setVideoAspectRatio(width, height) {
        screenVideoRect.aspectRatio = width / height
    }

    // Size of web view
    // These properties are read in messaging module
    // Cursor position relative to web view
    property int cursorX: 0
    property int cursorY: 0
    property bool captureCursor: false

    property var preferencesMenu: PreferencesMenu { }

    function getCaptureCursor() {
        return captureCursor;
    }

    function getCursorX() {
        // TODO: use parseInt()
        //return cursorX + parseInt(screenVideoRect.webView.x);
        return cursorX + screenVideoRect.webView.x;
    }

    function getCursorY() {
        return cursorY + screenVideoRect.webView.y;
    }

    function getVideoWidth () {
        return screenVideoRect.webView.width;
    }

    function getVideoHeight() {
        return screenVideoRect.webView.height;
    }

    // Setup locale domain
    property var dsslocale: DLocale {
        domain: "deepin-remote-assistance"
    }

    // Internationalization
    function dsTr(s){
        return dsslocale.dsTr(s)
    }

    NormalTitleBar {
        id: normalTitleBar
        anchors.top: parent.top
        visible: root.state === "normalMode"
        enabled: visible
        z: 0
    }

    FullscreenTitleBar {
        id: fullscreenTitleBar
        //anchors.top: parent.top
        visible: root.state === "fullscreenMode"
        enabled: visible
        z: 1
    }

    // web frame
    ScreenVideoRect {
        id: screenVideoRect
        anchors.top: normalTitleBar.bottom
        width: parent.width
        height: parent.height - normalTitleBar.height
    }

    states: [
        State {
            name: "normalMode"
            PropertyChanges {
                target: screenVideoRect
                anchors.top: normalTitleBar.bottom
                height: root.height - normalTitleBar.height
            }
        },

        State {
            name: "fullscreenMode"
            PropertyChanges {
                target: screenVideoRect
                //anchors.top: root.top
                anchors.top: normalTitleBar.top
                height: root.height
            }
        }
    ]
}

