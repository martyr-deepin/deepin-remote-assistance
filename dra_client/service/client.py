

'''
Controller for client side.

Start:
* Start WSSD

Stop:
* Stop WSSD
'''

from PyQt5.QtCore import QObject

from .wssd import WSSDController

class Client(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.wssd = None

    def start(self):
        self.start_wssd()

    def stop(self):
        self.stop_wssd()

    def start_wssd(self):
        print('[client] start wssd')
        if not self.wssd:
            self.wssd = WSSDController(self)
            self.wssd.start()

    def stop_wssd(self):
        print('[client] stop wssd')
        if self.wssd:
            self.wssd.stop()
