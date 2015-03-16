#!/usr/bin/env python3

import sys
sys.path.append('..')

from PyQt5.QtCore import QCoreApplication

from dra import wssd

app = QCoreApplication(sys.argv)

server = wssd.WSSD()
server.start()

app.exec()
