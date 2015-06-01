#!/usr/bin/env python3

import sys
sys.path.insert(0, '..')

from PyQt5 import QtCore

from dra_utils import network

app = QtCore.QCoreApplication([])
state = network.is_connected()
print('state:', state)
QtCore.QTimer.singleShot(1000, app.quit)
app.exec()
