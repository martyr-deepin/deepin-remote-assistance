#!/usr/bin/env python3

import sys
sys.path.insert(0, '..')

from PyQt5 import QtCore


from dra_utils import background
from dra_utils import process

app_path = '/usr/bin/gedit'
popen = background.launch_app_in_background([app_path])

@QtCore.pyqtSlot()
def kill_gedit():
    print('kill gedit now')
    process.pkill(app_path)
    app.exit()

app = QtCore.QCoreApplication([])

QtCore.QTimer.singleShot(2000, kill_gedit)
app.exec()
