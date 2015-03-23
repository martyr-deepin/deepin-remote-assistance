
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQml
from PyQt5 import QtQuick

from . import views


class MainWindowEngine(QtQml.QQmlApplicationEngine):

    def __init__(self):
        super().__init__()

        self.load(views.MAIN_WINDOW)
        #self.quit.connect(QtGui.QGuiApplication.instance().quit)

        # QtGui.QWindow
        self.window = self.rootObjects()[0]

        # To mark fullscreen state
        self.window.fullscreen = False

    def toggleFullscreen(self):
        if self.window.fullscreen:
            self.window.showNormal()
        else:
            self.window.showFullScreen()
        self.window.fullscreen = not self.window.fullscreen

    def show(self):
        self.window.fullscreenToggled.connect(self.toggleFullscreen)
        self.window.show()

