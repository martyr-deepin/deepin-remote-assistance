
'''Handle messages'''

import json

from PyQt5 import QtCore

from Xlib import X

from dra_utils.log import client_log
from . import constants

# mouse button orders
button_ids = (None, 1, 2, 3, 4, 5, 6, 7)

# To mark web page is loaded or not
remoting_connected = False

# Method to send messages to browser
def default_send_message(msgId, msg):
    client_log.warn('[messaging] default_send_message: %s, %s' % (msgId, msg))

send_message = default_send_message

# Reference to client dbus object
client_dbus = None

def init_send_message(sendMessage, clientDBus):
    client_log.debug('[messaging] init send_message: %s' % sendMessage)
    global send_message
    send_message = sendMessage
    global client_dbus
    client_dbus = clientDBus

def init_remoting(remote_peer_id):
    '''Connect to remote peer'''
    client_log.info('[messaging] init_remoting: %s' % remote_peer_id)
    send_message(constants.CMD_MSG, json.dumps({
        'Type': constants.CLIENT_MSG_INIT,
        'Payload': remote_peer_id,
    }))

def send_keyboard_event(event):
    #client_log.debug('send_keyboard_event: %s' % event)
    print('send keyboard event:', event, type(event))
    send_message(constants.KEYBOARD_MSG, event)


@QtCore.pyqtSlot("QVariant")
def handle_mouse_event(event):
    '''Listening mouse event and send it to browser'''
    try:
        if not remoting_connected:
            print('page not ready')
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
    send_message(constants.KEYBOARD_MSG, json.dumps(msg))

def handle_cmd_message(msg):
    '''Handle cmd messages'''
    try:
        msg = json.loads(msg)
    except ValueError as e:
        client_log.warn('[messaging] Warning: handle this error: %s' % e)
        return

    router = {
        constants.CLIENT_MSG_READY: constants.CLIENT_STATUS_PAGE_READY,
        constants.CLIENT_MSG_CONNECTED: constants.CLIENT_STATUS_CONNECT_OK,
        constants.CLIENT_MSG_UNAVAILABLE: constants.CLIENT_STATUS_UNAVAILABLE,
        constants.CLIENT_MSG_DISCONNECTED: constants.CLIENT_STATUS_DISCONNECTED,
    }

    if msg['Type'] == constants.CLIENT_MSG_READY:
        client_dbus.StatusChanged(constants.CLIENT_STATUS_PAGE_READY)
    elif msg['Type'] == constants.CLIENT_MSG_CONNECTED:
        client_dbus.StatusChanged(constants.CLIENT_STATUS_CONNECT_OK)
        global remoting_connected 
        remoting_connected = True
        try:
            video = json.loads(msg['Payload'])
        except ValueError as e:
            client_log.warn('[messaging] Failed to read video info: %s, %s' %
                    (e, msg['Payload']))
            return

        # Notify qml about video property
        client_dbus.main_window.root.screenVideoWidth = video['width']
        client_dbus.main_window.root.screenVideoHeight = video['height']

    elif msg['Type'] == constants.CLIENT_MSG_UNAVAILABLE:
        client_dbus.StatusChanged(constants.CLIENT_STATUS_UNAVAILABLE)
    elif msg['Type'] == constants.CLIENT_MSG_DISCONNECTED:
        client_dbus.StatusChanged(constants.CLIENT_STATUS_DISCONNECTED)
        # Kill host service after 1s
        QtCore.QTimer.singleShot(1000, client_dbus.Stop)
    else:
        lient_log.warn('[messaging] Warning: handle this message: %s' % msg)
