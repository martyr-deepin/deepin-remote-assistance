#!/usr/bin/env python3

import sys
sys.path.insert(0, '../..')

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from dra_client.service.keyboardcapture import CaptureController


class Form(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(320, 240)

        self.keyLabel = QtWidgets.QLabel()
        startButton = QtWidgets.QPushButton('&Start')
        stopButton = QtWidgets.QPushButton('Sto&p')

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(startButton)
        layout.addWidget(stopButton)
        layout.addWidget(self.keyLabel)
        self.setLayout(layout)

        self.captureController = CaptureController(self)

        startButton.clicked.connect(self.captureController.capture)
        stopButton.clicked.connect(self.captureController.uncapture)

        self.setWindowTitle('Grab Global Keyboard Event')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def focusInEvent(self, event):
        print('focus in event:', event)

    def focusOutEvent(self, event):
        print('focus out event:', event)

    def event(self, event):
        print('event:', event)
        return QtWidgets.QDialog.event(self, event)

def main():
    app = QtWidgets.QApplication(sys.argv)

    form = Form()
    form.show()

    app.exec()

if __name__ == '__main__':
    main()
