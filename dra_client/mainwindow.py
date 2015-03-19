
from PyQt5 import QtCore
from PyQt5 import QtQuick

from . import views


class MainWindow(QtQuick.QQuickView):

    def __init__(self):
        super().__init__()

        print(views.MAIN_WINDOW)
        print(QtCore.QUrl.fromLocalFile(views.MAIN_WINDOW))
        self.setSource(QtCore.QUrl.fromLocalFile(views.MAIN_WINDOW))
