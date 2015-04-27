

'''
Controller for client side.

Start:
* Start WSSD

Stop:
* Stop WSSD
'''

from PyQt5.QtCore import QObject

from .wssd import WSSDController
from . import clipboard
from . import cmd
from . import mouse

class Client(QObject):

    def __init__(self, client_dbus):
        super().__init__()
        self.wssd = None

        # Init event handlers
        cmd.init(client_dbus)
        mouse.init(client_dbus)
        clipboard.init(client_dbus)

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
