#!/usr/bin/env python3

import sys
sys.path.insert(0, '../..')

from PyQt5 import QtWidgets

from dra_server.views.disconnectwindow import DisconnectWindow

app = QtWidgets.QApplication([])
disconnect_window = DisconnectWindow(None)
disconnect_window.disconnected.connect(app.quit)
disconnect_window.show()
app.exec()


