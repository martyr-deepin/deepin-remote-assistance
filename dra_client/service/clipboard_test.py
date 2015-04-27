#!/usr/bin/env python3

import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

def handle():
    text = clip.text(QtGui.QClipboard.Clipboard)
    if text:
        print('text:', text)
    pixmap = clip.pixmap(QtGui.QClipboard.Clipboard)
    if pixmap:
        print('pixmap:', pixmap)
        print(hasattr(pixmap, 'QVariant'))

app = QtWidgets.QApplication(sys.argv)
clip = app.clipboard()
print(clip)
clip.dataChanged.connect(handle)
app.exec()
