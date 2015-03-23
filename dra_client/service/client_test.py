#!/usr/bin/env python3

import sys
sys.path.insert(0, '../..')

from PyQt5 import QtWidgets

from dra_client.service.client import Client


class Form(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        initButton = QtWidgets.QPushButton('&Init')
        captureButton = QtWidgets.QPushButton('&Capture')
        uncaptureButton = QtWidgets.QPushButton('&Uncapture')

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(initButton)
        layout.addWidget(captureButton)
        layout.addWidget(uncaptureButton)
        self.setLayout(layout)

        self.setWindowTitle('Client Side')

        self.client = Client(self)
        initButton.clicked.connect(self.client.start)
        captureButton.clicked.connect(self.client.capture)
        uncaptureButton.clicked.connect(self.client.uncapture)

    def focusInEvent(self, event):
        print('focus in')

    def focusOutEvent(self, event):
        print('focus out')


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec()

if __name__ == '__main__':
    main()
