#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication

from dra_client.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
