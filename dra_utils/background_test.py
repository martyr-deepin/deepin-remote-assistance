#!/usr/bin/env python3

from PyQt5 import QtCore

import background

popen = background.launch_app_in_background(['gedit'])

app = QtCore.QCoreApplication([])
app.exec()
