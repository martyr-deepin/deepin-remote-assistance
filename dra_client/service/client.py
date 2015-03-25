

'''
Controller for client side.

Start:
* Start WSSD
* Start keyboard capture

Stop:
* Stop keyboard capture
* Stop WSSD
'''

from PyQt5.QtCore import QObject

from .keyboardcapture import CaptureController
from .wssd import WSSDController
from . import keyboard

class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.wssd = None
        self.keyboard_capture = None

    def start(self):
        self.start_wssd()
        self.start_keyboard_capture()

    def stop(self):
        self.stop_wssd()
        self.stop_keyboard_capture()

    def start_wssd(self):
        self.stop_wssd()
        self.wssd = WSSDController(self)
        self.wssd.start()

    def start_keyboard_capture(self):
        self.stop_keyboard_capture()
        self.keyboard_capture = CaptureController(self)

    def stop_wssd(self):
        if self.wssd:
            self.wssd.stop()
            self.wssd = None

    def stop_keyboard_capture(self):
        if self.keyboard_capture:
            self.keyboard_capture.stop()
            self.keyboard_capture = None

    def try_capture(self):
        print('try capture')
        if keyboard.keyboard_conn:
            self.capture()

    def capture(self):
        print('client.capture()')
        if self.keyboard_capture:
            self.keyboard_capture.capture()
        else:
            print('Keyboard capture is uninitialized!')

    def uncapture(self):
        print('client.uncapture()')
        if self.keyboard_capture:
            self.keyboard_capture.uncapture()
        else:
            print('keyboard capture is uninitialized!')
