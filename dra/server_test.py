#!/usr/bin/env python3

import sys
sys.path.append('..')

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QTimer

from dra.server import Server

class Form(QForm):

    def __init__(self, parent=

app = QApplication(sys.argv)

s = Server()
s.start()

form = Form()
form.show()

app.exec()
