
import json

from PyQt5 import QtCore
import tornado.websocket
from Xlib import X

from dra_utils.log import client_log

# mouse button orders
button_ids = (None, 1, 2, 3, 4, 5, 6, 7)

def init(client_dbus_):
    '''Init client_dbus instance'''
    global client_dbus
    client_dbus = client_dbus_

client_dbus = None

def send_message(msg):
    '''Send mouse message to browser'''
    if not connection:
        client_log.debug('[mouse] connection uninitialized')
        return
    connection.write_message(msg)

@QtCore.pyqtSlot("QVariant")
def handle_mouse_event(event):
    '''Listening mouse event and send it to browser'''
    try:
        if not client_dbus or not client_dbus.remoting_connected:
            return
        if not client_dbus.main_window.root.getCaptureCursor():
            return
        offsetX = client_dbus.main_window.root.getCursorX()
        offsetY = client_dbus.main_window.root.getCursorY()
        width = client_dbus.main_window.root.getVideoWidth()
        height = client_dbus.main_window.root.getVideoHeight()
    except AttributeError as e:
        print(e)
        return

    # TODO: simplify this method
    if event.type == X.ButtonPress:
        msg = {
            'type': 'press',
            'button': button_ids[event.detail],
            'x': event.root_x,
            'y': event.root_y,
            'offsetX': offsetX,
            'offsetY': offsetY,
            'w': width,
            'h': height,
        }
    elif event.type == X.ButtonRelease:
        msg = {
            'type': 'release',
            'button': button_ids[event.detail],
            'x': event.root_x,
            'y': event.root_y,
            'offsetX': offsetX,
            'offsetY': offsetY,
            'w': width,
            'h': height,
        }
    else:
        msg = {
            'type': 'move',
            'x': event.root_x,
            'y': event.root_y,
            'offsetX': offsetX,
            'offsetY': offsetY,
            'w': width,
            'h': height,
        }
    send_message(json.dumps(msg))

connection = None

class MouseWebSocket(tornado.websocket.WebSocketHandler):
    '''mouse message handler'''

    def on_open(self):
        global connection
        connection = self
