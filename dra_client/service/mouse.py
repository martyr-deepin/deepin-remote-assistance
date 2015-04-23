
import json

from PyQt5 import QtCore
import tornado.websocket
from Xlib import X

from dra_utils.log import client_log

# mouse button orders
button_ids = (None, 1, 3, 2, 4, 5, 6, 7)

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

    msg = {
        'type': event.type,
        'x': offsetX,
        'y': offsetY,
        'w': width,
        'h': height,
    }
    if event.type == X.ButtonPress or event.type == X.ButtonRelease:
        msg['button'] = button_ids[event.detail]
    elif event.type != X.MotionNotify:
        # Ignore KeyPress/KeyRelease event
        return
    print(msg)
    send_message(json.dumps(msg))

connection = None

class MouseWebSocket(tornado.websocket.WebSocketHandler):
    '''mouse message handler'''

    def open(self):
        global connection
        connection = self
