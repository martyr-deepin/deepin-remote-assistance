#!/usr/bin/env python3

import sys
sys.path.insert(0, '..')

from PyQt5 import QtCore
from dra_server.chromium import Chromium

app = QtCore.QCoreApplication(sys.argv)

cr = Chromium()
cr.start()

app.exec()
