
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick
from PyQt5 import QtWidgets

from . import views
from .service.client import Client
from .service import mouse
from .utils.event import EventHandler
from .utils.event import EventRecord

class MainWindow(QtQuick.QQuickView):

    def __init__(self):
        QtQuick.QQuickView.__init__(self)

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

    def toggleFullscreen(self):
        # TODO: remove this method
        print('toggle fullscreen')
        return
        if self.window.fullscreen:
            self.window.showNormal()
        else:
            self.window.showFullScreen()
        self.window.fullscreen = not self.window.fullscreen

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
