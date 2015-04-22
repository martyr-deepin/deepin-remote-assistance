#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2014 Deepin, Inc.
#               2011~2014 Kaisheng Ye
#
# Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
# Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from Xlib import X

from . import xrobot

class EventRecord(QThread):

    captureEvent = pyqtSignal("QVariant")

    def __init__(self):
        QThread.__init__(self)

    def record_callback(self, reply):
        xrobot.check_valid_event(reply)

        data = reply.data
        while len(data):
            event, data = xrobot.get_event_data(data)
            self.captureEvent.emit(event)

    def run(self):
        xrobot.record_event(self.record_callback)

class EventHandler(QObject):

    keyPressed = pyqtSignal(str, arguments=["keyname",])
    keyReleased = pyqtSignal(str, arguments=["keyname",])
    buttonPressed = pyqtSignal(int, int, int, arguments=["x", "y", "time"])
    buttonReleased = pyqtSignal(int, int, int, arguments=["x", "y", "time"])
    cursorPositionChanged = pyqtSignal(int, int, arguments=["x", "y"])

    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot("QVariant")
    def handle_event(self, event):

        # KeyPress event
        if event.type == X.KeyPress:
            keyname = xrobot.get_keyname(event)
            self.keyPressed.emit(keyname)

        # KeyRelease event
        elif event.type == X.KeyRelease:
            keyname = xrobot.get_keyname(event)
            self.keyReleased.emit(keyname)

        # ButtonPress event
        elif event.type == X.ButtonPress:
            self.buttonPressed.emit(event.root_x, event.root_y, event.time)

        # ButtonRelease event
        elif event.type == X.ButtonRelease:
            self.buttonReleased.emit(event.root_x, event.root_y, event.time)

        # MotionNotify event
        elif event.type == X.MotionNotify:
            self.cursorPositionChanged.emit(event.root_x, event.root_y)

