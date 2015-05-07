#!/usr/bin/env python3

import sys
sys.path.insert(0, '../..')

from PyQt5 import QtWidgets

from dra_server.views.confirmwindow import ConfirmWindow

app = QtWidgets.QApplication([])
confirm_window = ConfirmWindow(None)
confirm_window.show()
app.exec()


