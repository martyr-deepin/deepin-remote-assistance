
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQml
from PyQt5 import QtQuick

from . import views
from .service.client import Client


class MainWindowEngine(QtQml.QQmlApplicationEngine):

    def __init__(self):
        super().__init__()

        self.load(views.MAIN_WINDOW)
        #self.quit.connect(QtGui.QGuiApplication.instance().quit)

        # QtGui.QWindow
        self.window = self.rootObjects()[0]

        # To mark fullscreen state
        self.window.fullscreen = False

        #self.host_client = Client(self)
        self.host_client = Client()

    def toggleFullscreen(self):
        if self.window.fullscreen:
            self.window.showNormal()
        else:
            self.window.showFullScreen()
        self.window.fullscreen = not self.window.fullscreen

    def onMainWindowFocusChanged(self):
        print('window is active:', self.window.isActive())
        if self.window.isActive():
            self.host_client.try_capture()
        else:
            self.host_client.uncapture()

    def show(self):
        self.window.fullscreenToggled.connect(self.toggleFullscreen)
        self.window.activeChanged.connect(self.onMainWindowFocusChanged)
        self.window.show()

        self.host_client.start()
