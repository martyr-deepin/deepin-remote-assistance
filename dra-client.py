#!/usr/bin/env python3

import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from dra_client.mainwindowengine import MainWindowEngine

def main():
    app = QGuiApplication(sys.argv)

    engine = MainWindowEngine()
    engine.show()

    app.exec()

if __name__ == '__main__':
    main()
