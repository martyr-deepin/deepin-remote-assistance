
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick

from dra_server import views

class ConfirmWindow(QtQuick.QQuickView):

    accepted = QtCore.pyqtSignal()
    rejected = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        rootContext = self.rootContext()
        rootContext.setContextProperty('windowView', self)

        self.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        surface_format = QtGui.QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)
        self.setFormat(surface_format)
        self.setColor(QtGui.QColor(0, 0, 0, 0))
        self.setFlags(QtCore.Qt.FramelessWindowHint |
                      QtCore.Qt.Window |
                      QtCore.Qt.WindowStaysOnTopHint)

        self.setSource(QtCore.QUrl.fromLocalFile(views.CONFIRM_WINDOW))

