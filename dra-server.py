#!/usr/bin/env python3

import json
import sys
sys.path.append('..')

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from dra_server.server import Server
from dra_server import constants

class Form(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        #self.server = Server(self)
        self.server = Server()

        startButton = QPushButton('&Start')
        stopButton = QPushButton('Sto&p')
        startButton.clicked.connect(self.server.start)
        self.server.peerIdUpdated.connect(self.updatePeerId)
        stopButton.clicked.connect(self.server.stop)
        self.id_edit = QLineEdit()
        self.id_edit.setReadOnly(True)

        layout = QHBoxLayout()
        layout.addWidget(startButton)
        layout.addWidget(stopButton)
        layout.addWidget(self.id_edit)
        self.setLayout(layout)

    def updatePeerId(self, peerId):
        self.id_edit.setText(peerId)

app = QApplication(sys.argv)

form = Form()
form.show()

app.exec()
