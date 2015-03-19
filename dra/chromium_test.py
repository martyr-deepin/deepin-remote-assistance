#!/usr/bin/env python3

import sys
sys.path.append('..')

from PyQt5 import QtCore
from dra.chromium import Chromium

app = QtCore.QCoreApplication(sys.argv)

cr = Chromium()
cr.start()

app.exec()
