#!/usr/bin/env python3

import json
import sys
sys.path.append('..')

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from dra import wssd

def print_cmd(msg):
    print('print cmd:', msg)

class Form(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.server = wssd.WSSDController()
        self.server.worker.browserCmd.connect(self.handle_cmd_event)

        startButton = QPushButton('&Start')
        stopButton = QPushButton('Sto&p')
        startButton.clicked.connect(self.server.start)
        stopButton.clicked.connect(self.server.stop)
        self.id_edit = QLineEdit()
        self.id_edit.setReadOnly(True)

        layout = QHBoxLayout()
        layout.addWidget(startButton)
        layout.addWidget(stopButton)
        layout.addWidget(self.id_edit)
        self.setLayout(layout)
    
    def handle_cmd_event(self, msg):
        print('handle cmd event:', msg)
        # TODO: catch exception
        event = json.loads(msg)
        # TODO: check msg type
        self.id_edit.setText(event['id'])

def main():
    app = QApplication(sys.argv)

    form = Form()
    form.show()

    app.exec()

if __name__ == '__main__':
    main()
