#!/usr/bin/env python3

import sys
sys.path.insert(0, '..')

from PyQt5 import QtWidgets

from dra_server.controlpanel import ControlPanel

app = QtWidgets.QApplication([])
control_panel = ControlPanel()
control_panel.show()
app.exec()

