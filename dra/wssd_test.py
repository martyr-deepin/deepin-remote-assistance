#!/usr/bin/env python3

import sys

from PyQt5.QtCore import QCoreApplication

import wssd


app = QCoreApplication(sys.argv)

server = wssd.WSSD()
server.start()

app.exec()
