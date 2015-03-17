#!/usr/bin/env python3

import sys
sys.path.append('..')

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton

from dra import wssd

def print_cmd(msg):
    print('cmd:', msg)
    return []

class Form(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.server = wssd.WSSDController()
        self.server.worker.browserCmd.connect(print_cmd)

        startButton = QPushButton('&Start')
        stopButton = QPushButton('Sto&p')
        startButton.clicked.connect(self.server.start)
        stopButton.clicked.connect(self.server.stop)

        layout = QHBoxLayout()
        layout.addWidget(startButton)
        layout.addWidget(stopButton)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)

    #form = Form()
    #form.show()
    server = wssd.WSSDController()
    server.start()

    app.exec()

if __name__ == '__main__':
    main()
