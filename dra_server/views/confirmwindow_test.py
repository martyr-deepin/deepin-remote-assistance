#!/usr/bin/env python3

import sys
sys.path.insert(0, '../..')

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from dra_server.views.confirmwindow import ConfirmWindow
from dra_utils.constants import ICON_PATH

app = QtWidgets.QApplication([])
app.setWindowIcon(QtGui.QIcon(ICON_PATH))
confirm_window = ConfirmWindow(None)
confirm_window.show()
app.exec()


