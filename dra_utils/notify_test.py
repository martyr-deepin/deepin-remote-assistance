#!/usr/bin/env python3

import sys
sys.path.insert(0, '..')

from PyQt5 import QtCore

from dra_utils.notify import notify

app = QtCore.QCoreApplication([])
notify('Hello')
app.exec()
