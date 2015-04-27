
from PyQt5 import QtCore

from .chromium import Chromium
from . import clipboard
from . import cmd
from . import constants
from . import keyboard
from .wssd import WSSDController
from dra_utils.log import server_log

'''
Controller for server side.

Start:
    * start websocket
    * start chromium

Stop:
    * stop chromium
    * stop websocket
'''

class Server(QtCore.QObject):

    def __init__(self, server_dbus):
        super().__init__()
        self.wssd = None
        self.chromium = None

        # Init event handlers
        cmd.init(server_dbus)
        clipboard.init(server_dbus)

    def start(self):
        '''Start desktop sharing service'''
        self.start_wssd()
        self.start_chromium()

    def stop(self):
        '''Stop desktop sharing service'''
        self.stop_chromium()
        self.stop_wssd()
        keyboard.reset_keyboard()

    def start_wssd(self):
        '''Start websocket service'''
        self.stop_wssd()
        self.wssd = WSSDController(self)
        self.wssd.start()

    def stop_wssd(self):
        '''Stop websocket service'''
        if self.wssd:
            self.wssd.stop()

    def start_chromium(self):
        '''Launch chromium in background'''
        self.stop_chromium()
        self.chromium = Chromium(self)
        self.chromium.start()

    def stop_chromium(self):
        '''Kill chromium'''
        if self.chromium:
            self.chromium.stop()

