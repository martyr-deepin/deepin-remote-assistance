
import json

from PyQt5 import QtCore

from dra_utils import ByPassOriginWebSocketHandler
from dra_utils.log import client_log

@QtCore.pyqtSlot(str)
def send_message(msg):
    '''Send keyboard messages to browsesr'''
    if not connection:
        client_log.debug('[keyboard] connection is uninitialized')
        return
    connection.write_message(msg)

connection = None

class KeyboardWebSocket(ByPassOriginWebSocketHandler):
    '''Keyboard message handler'''

    def open(self):
        global connection
        connection = self
