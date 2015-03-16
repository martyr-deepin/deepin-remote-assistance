
from PyQt5.QtCore import QObject
from dra.chromium import Chromium
from dra.wssd import WSSD

'''
Controller for service side.

Start:
    * start websocket
    * start chromium

Stop:
    * stop chromium
    * stop websocket
'''


class Server(QObject):

    def __init__(self):
        super().__init__()
        self.wssd = None
        self.chromium = None

    def start(self):
        '''Start desktop sharing service'''
        self.start_wssd()
        self.start_chromium()

    def stop(self):
        '''Stop desktop sharing service'''
        self.stop_chromium()
        self.stop_wssd()

    def start_wssd(self):
        '''Start websocket service'''
        self.stop_wssd()
        self.wssd = WSSD()
        self.wssd.start()

    def stop_wssd(self):
        '''Stop websocket service'''
        if self.wssd:
            self.wssd.terminate()

    def start_chromium(self):
        '''Launch chromium in background'''
        self.stop_chromium()
        self.chromium = Chromium()
        self.chromium.start()

    def stop_chromium(self):
        '''Kill chromium'''
        if self.chromium:
            self.chomium.stop()
