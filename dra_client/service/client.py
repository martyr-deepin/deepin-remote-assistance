

'''
Controller for client side.

Start:
* Start keyboard capture
* Start WSSD

Stop:
* Stop keyboard capture
* Stop WSSD
'''

from PyQt5.QtCore import QObject

from .keyboardcapture import KeyboardCaptureController
from .wssd import WSSDController

class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.keyboard_capture = None
        self.wssd = None

    def start(self):
        self.start_keyboard_capture()
        self.start_wssd()

    def stop(self):
        self.stop_keyboard_capture()
        self.stop_wssd()

    def start_keyboard_capture(self):
        self.stop_keyboard_capture()
        self.keyboard_capture = KeyboardCaptureController(self)

    def stop_keyboard_capture(self):
        if self.keyboard_capture:
            self.keyboard_capture.stop()
            self.keyboard_capture = None

    def start_wssd(self):
        print('[client] start wssd')
        if not self.wssd:
            self.wssd = WSSDController(self)
            self.wssd.start()

    def stop_wssd(self):
        print('[client] stop wssd')
        if self.wssd:
            self.wssd.stop()

    def try_capture(self):
        print('try capture')
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
