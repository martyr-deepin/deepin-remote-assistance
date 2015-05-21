#!/usr/bin/env python3

import sys
sys.path.insert(0, '..')

from PyQt5 import QtCore

from dra_utils import background

popen = background.launch_app_in_background(['gedit'])

app = QtCore.QCoreApplication([])
app.exec()
