
import json

import tornado.websocket
from PyQt5 import QtCore

from dra_utils.log import client_log

@QtCore.pyqtSlot(str)
def send_message(msg):
    '''Send keyboard messages to browsesr'''
    if not connection:
        client_log.debug('[keyboard] connection is uninitialized')
        return
    connection.write_message(msg)

connection = None

class KeyboardWebSocket(tornado.websocket.WebSocketHandler):
    '''Keyboard message handler'''

    def on_open(self):
        global connection
        connection = self
