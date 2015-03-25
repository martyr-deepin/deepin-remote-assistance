#!/usr/bin/env python3

import sys
sys.path.insert(0, '../..')
import time

from PyQt5 import QtWidgets

from dra_client.service.wssd import WSSDController
from dra_client.service import keyboard 


app = QtWidgets.QApplication(sys.argv)
client = WSSDController()
client.start()

i = 0
while True:
    keyboard.send_event(str(i))
    i = i + 1
    time.sleep(1)

app.exec()
