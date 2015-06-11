
import json

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick
from PyQt5 import QtWidgets

from dra_client import views
from dra_client.service.client import Client
from dra_client.service import keyboard
from dra_client.service import mouse
from dra_client.utils.event import EventHandler
from dra_client.utils.event import EventRecord
from dra_utils.constants import ICON_PATH

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

        rootContext = self.rootContext()
        rootContext.setContextProperty('windowView', self)
        rootContext.setContextProperty('eventHandler', self._event_handler)

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

        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setIcon(QtGui.QIcon(ICON_PATH))
        self.tray.activated.connect(self.onSystemTrayActivated)

        self.visibilityChanged.connect(self.onVisibilityChanged)

        # Old visiblity of window
        self.oldVisibility = QtGui.QWindow.Windowed

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

    @QtCore.pyqtSlot(QtCore.QVariant)
    def onWindowFocusChanged(self, window):
        self.setKeyboardGrabEnabled(window is not None)

    @QtCore.pyqtSlot()
    def toggleFullscreen(self):
        '''Toggle window status between fullscreen and normal'''
#        if self.visibility() != QtGui.QWindow.FullScreen:
#            #self.showFullScreen()
#            self.setVisibility(QtGui.QWindow.FullScreen)
#        else:
#            self.setVisibility(QtGui.QWindow.Windowed)
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
        else:
            self.setVisibility(QtGui.QWindow.Windowed)

    @QtCore.pyqtSlot()
    def closeToSystemTray(self):
        '''Close to system tray'''
        self.setVisible(False)

    @QtCore.pyqtSlot(QtCore.QVariant)
    def onSystemTrayActivated(self, reason):
        self.setVisible(not self.isVisible())

    def onVisibilityChanged(self, visibility):
        if visibility == 3:
            self.setVisible(False)

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
        self.tray.show()
        self.oldVisibility = self.visibility()
