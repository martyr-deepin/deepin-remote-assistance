
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick

from . import views

class ControlPanel(QtQuick.QQuickView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        surface_format = QtGui.QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)
        self.setFormat(surface_format)
        self.setColor(QtGui.QColor(0, 0, 0, 0))
        self.setFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

        self.setSource(QtCore.QUrl.fromLocalFile(views.CONTROL_PANEL))
        self.root = self.rootObject()
