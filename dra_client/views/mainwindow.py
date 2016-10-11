
import json

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick
from PyQt5 import QtWidgets

from dra_client import views
from dra_client.service.client import Client
from dra_client.service import cmd
from dra_client.service import keyboard
from dra_client.service import mouse
from dra_client.utils.event import EventHandler
from dra_client.utils.event import EventRecord
from dra_utils.constants import ICON_PATH
from .preferencesmenu import PreferencesMenu

class MainWindow(QtQuick.QQuickView):

    # Emit window closed signal when close button is clicked
    windowClosed = QtCore.pyqtSignal()

    def __init__(self):
        QtQuick.QQuickView.__init__(self)

        self.setIcon(QtGui.QIcon(ICON_PATH))

        self._event_handler = EventHandler()
        self._event_handler.cursorPositionChanged.connect(
                self._record_cursor_position)
        self._event_record = EventRecord()
        self._event_record.captureEvent.connect(
                self._event_handler.handle_event)
        # Mouse event 
        self._event_record.captureEvent.connect(mouse.handle_mouse_event)

        self.preferencesMenu = PreferencesMenu()
        rootContext = self.rootContext()
        rootContext.setContextProperty('windowView', self)
        rootContext.setContextProperty('eventHandler', self._event_handler)
        rootContext.setContextProperty('preferencesMenu',
                                       self.preferencesMenu)

        # Do not kill qApp when main window is closed, instead emiting a 
        #window-closed signal so that client dbus can send
        # a STATUS_STOPPED signal to control panel
        QtWidgets.qApp.setQuitOnLastWindowClosed(False)

        self.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        surface_format = QtGui.QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)
        self.setFormat(surface_format)
        self.setColor(QtGui.QColor(0, 0, 0, 0))
        self.setFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

        self.setSource(QtCore.QUrl.fromLocalFile(views.MAIN_WINDOW))
        self.root = self.rootObject()
        QtWidgets.qApp.focusWindowChanged.connect(self.onWindowFocusChanged)
        self.root.screenLevelChanged.connect(self.onScreenLevelChanged)

        # Old visiblity of window
        self.oldVisibility = QtGui.QWindow.Windowed

        self.maxButtonClicked = False
        self.requireMaximized = False
        self.windowStateChanged.connect(self.onWindowStateChanged)

    def keyPressEvent(self, event):
        keyboard.send_message(json.dumps({
            'press': True,
            'code': event.nativeScanCode(),
        }))

    def keyReleaseEvent(self, event):
        keyboard.send_message(json.dumps({
            'press': False,
            'code': event.nativeScanCode(),
        }))

    @QtCore.pyqtSlot()
    def close(self):
        self.windowClosed.emit()
        super().close()

    @QtCore.pyqtSlot("QWindow*")
    def onWindowFocusChanged(self, window):
        self.setKeyboardGrabEnabled(window is not None)

    @QtCore.pyqtSlot(int)
    def onScreenLevelChanged(self, level):
        cmd.reset_screen_level(level)

    @QtCore.pyqtSlot()
    def toggleFullscreen(self):
        '''Toggle window status between fullscreen and normal'''
        if self.visibility() != QtGui.QWindow.FullScreen:
            self.oldVisibility = self.visibility()
            self.setVisibility(QtGui.QWindow.FullScreen)
        else:
            self.setVisibility(self.oldVisibility)

    @QtCore.pyqtSlot(result=bool)
    def isFullscreen(self):
        '''Check window is in fullscreen mode or not'''
        return self.visibility() == QtGui.QWindow.FullScreen

    @QtCore.pyqtSlot()
    def toggleMaximized(self):
        '''Toggle window status between maximized and normal'''
        if self.visibility() != QtGui.QWindow.Maximized:
            self.setVisibility(QtGui.QWindow.Maximized)
            self.maxButtonClicked = True
        else:
            self.setVisibility(QtGui.QWindow.Windowed)
            self.maxButtonClicked = False

    @QtCore.pyqtSlot()
    def minimize(self):
        self.setVisibility(QtGui.QWindow.Minimized)

    def onWindowStateChanged(self, state):
        #To fix window state change bug in Qt5.3 and Qt5.4
        if self.requireMaximized:
            self.windowStateChanged.disconnect(self.onWindowStateChanged)
            self.setVisibility(QtGui.QWindow.Maximized)
            self.windowStateChanged.connect(self.onWindowStateChanged)
            self.requireMaximized = False
            return
        if (self.visibility() == QtGui.QWindow.Windowed and
            self.maxButtonClicked and
            state == QtCore.Qt.WindowMinimized):
            self.requireMaximized = True
        else:
            self.requireMaximized = False

    @QtCore.pyqtSlot(int, int)
    def _record_cursor_position(self, x, y):
        self._cursor_pos = QtCore.QPoint(x, y)

    @QtCore.pyqtSlot(result=QtCore.QVariant)
    def getCursorPos(self):
        return self._cursor_pos

    @QtCore.pyqtSlot(result=QtCore.QVariant)
    def getGeometry(self):
        return self.geometry()

    def show(self):
        self._event_record.start()
        QtQuick.QQuickView.show(self)
        self.oldVisibility = self.visibility()

    @QtCore.pyqtSlot(int, int)
    def popupPreferencesMenu(self, x, y):
        '''Popup preferences menu at bottom of pref-button'''
        self.preferencesMenu.move(self.x() + x, self.y() + y)
        self.preferencesMenu.show()
