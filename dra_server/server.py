
import json

from PyQt5 import QtCore

from .chromium import Chromium
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

    def __init__(self, server_dbus, parent=None):
        super().__init__(parent=parent)
        self.wssd = None
        self.chromium = None
        self.server_dbus = server_dbus

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
        self.wssd.worker.browserCmd.connect(self.handleBrowserCmd)

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

    def handleBrowserCmd(self, msg):
        '''Handle command message sent from browser side.

        Some of these messages will be converted to Qt mssage'''
        print('handle browser cmd message:', msg)
        server_log.debug('handleBrowserCmd: %s' % msg)
        msg = json.loads(msg)

        if msg['Type'] == constants.SERVER_MSG_ECHO:
            self.server_dbus.peer_id_changed(msg['Payload'])
        elif msg['Type'] == constants.SERVER_MSG_SHARING:
            self.server_dbus.StatusChanged(constants.SERVER_STATUS_SHARING)
        elif msg['Type'] == constants.SERVER_MSG_DISCONNECT:
            self.server_dbus.StatusChanged(constants.SERVER_STATUS_DISCONNECTED)
            # Kill host service after 1s
            QtCore.QTimer.singleShot(1000, self.server_dbus.Stop)
        else:
            server_log.warn('handleBrowserCmd msg invalid: %s' % msg)
