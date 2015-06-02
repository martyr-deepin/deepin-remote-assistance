#!/usr/bin/env python3

import sys
sys.path.insert(0, '../..')

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from dra_server.views.disconnectwindow import DisconnectWindow
from dra_utils.constants import APP_NAME
from dra_utils.constants import ICON_PATH

app = QtWidgets.QApplication([])
app.setWindowIcon(QtGui.QIcon(ICON_PATH))
app.setApplicationName(APP_NAME)
disconnect_window = DisconnectWindow(None)
disconnect_window.disconnected.connect(app.quit)
disconnect_window.show()
app.exec()


