#!/usr/bin/env python3

import sys
sys.path.insert(0, '..')

from PyQt5 import QtCore

from dra_utils.screensaver import ScreenSaver

if __name__ == '__main__':
    app = QtCore.QCoreApplication([])
    s = ScreenSaver()
    print('check:', s.check())
    sid = s.inhibit()
    print('sid:', sid)
    app.exec()
