
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick

from dra_server import views
from dra_server.views.confirmwindow import ConfirmWindow
from dra_utils.constants import ICON_PATH

class DisconnectWindow(QtQuick.QQuickView):
    '''DisconnectWindow is used to terminate remoting service explicitly.'''

    # This signal is emitted when user confirms to terminate remote desktop
    # connection.
    disconnected = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setIcon(QtGui.QIcon(ICON_PATH))
        
        rootContext = self.rootContext()
        rootContext.setContextProperty('windowView', self)

        self.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        surface_format = QtGui.QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)
        self.setFormat(surface_format)
        self.setColor(QtGui.QColor(0, 0, 0, 0))
        self.setFlags(QtCore.Qt.SplashScreen |
                      QtCore.Qt.WindowStaysOnTopHint)

        self.setSource(QtCore.QUrl.fromLocalFile(views.DISCONNECT_WINDOW))

        # When `Disconnect` button clicked, show a confirmation dialog
        root = self.rootObject()
        root.disconnected.connect(self.showConfirmWindow)

        self.confirm_window = None

        QtCore.QCoreApplication.instance().aboutToQuit.connect(
                self.disconnected)

    @QtCore.pyqtSlot(result=QtCore.QVariant)
    def getCursorPos(self):
        '''This method is used to get cursor position in DDragArea'''
        return QtGui.QCursor.pos()

    @QtCore.pyqtSlot()
    def showConfirmWindow(self):
        '''Show a confirmation dialog now'''
        self.confirm_window = ConfirmWindow()
        self.confirm_window.accepted.connect(self.disconnected)
        self.confirm_window.show()
        self.confirm_window.raise_()
