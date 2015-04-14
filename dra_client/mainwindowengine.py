
from PyQt5 import QtQml
from PyQt5 import QtWidgets

from . import views
from .service.client import Client
from .service import messaging


class MainWindowEngine(QtQml.QQmlApplicationEngine):

    def __init__(self, client_dbus):
        super().__init__()

        self.load(views.MAIN_WINDOW)
        QtWidgets.qApp.setQuitOnLastWindowClosed(False)

        # QtGui.QWindow
        self.window = self.rootObjects()[0]

        # To mark fullscreen state
        self.window.fullscreen = False
        messaging.init_send_message(self.window.sendMessage, client_dbus)

        self.host_client = Client(self)

    def toggleFullscreen(self):
        return
        if self.window.fullscreen:
            self.window.showNormal()
        else:
            self.window.showFullScreen()
        self.window.fullscreen = not self.window.fullscreen

    def onMainWindowFocusChanged(self):
        print('window is active:', self.window.isActive())
        return
        if self.window.isActive():
            self.host_client.try_capture()
        else:
            self.host_client.uncapture()

    def cmdMessageReceived(self, msg):
        print('TODO: MainEngine. cmdMessage received:', msg)

    def onQuit(self):
        print('Main engine quit')

    def show(self):
        self.window.activeChanged.connect(self.onMainWindowFocusChanged)
        self.window.cmdMessaged.connect(messaging.handle_cmd_message)
        self.window.fullscreenToggled.connect(self.toggleFullscreen)
        self.host_client.start()
        self.window.show()
