
import json

from PyQt5 import QtCore
import tornado.websocket

from dra_utils.log import client_log
from . import constants

def init(client_dbus_):
    '''Init client_dbus instance'''
    global client_dbus
    client_dbus = client_dbus_

client_dbus = None

def send_message(msg):
    '''Send command message to browser'''
    if not connection:
        client_log.debug('[cmd] connection is uninitialized')
        return
    connection.write_message(msg)

def init_remoting(remote_peer_id):
    '''Connect to remote peer'''
    client_log.info('[cmd] init_remoting: %s' % remote_peer_id)
    send_message(json.dumps({
        'Type': constants.CLIENT_MSG_INIT,
        'Payload': remote_peer_id,
    }))

@QtCore.pyqtSlot(str)
def handle(msg):
    '''Handle cmd messages'''
    if not client_dbus:
        client_log.warn('[cmd] client dbus is uninitialized')
        return
    try:
        msg = json.loads(msg)
    except ValueError as e:
        client_log.warn('[cmd] Warning: handle this error: %s' % e)
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
        try:
            video = json.loads(msg['Payload'])
        except ValueError as e:
            client_log.warn('[cmd] Failed to read video info: %s, %s' %
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
        lient_log.warn('[cmd] Warning: handle this message: %s' % msg)

class Emitter(QtCore.QObject):
    '''Emitter class is used to send cmdReceived signal.

    That signal shall be handled in UI thread'''

    cmdReceived = QtCore.pyqtSignal(str)
    
emitter = Emitter()
emitter.cmdReceived.connect(handle)

# This object is used to send message to browser
# CGeck connection and call connection.write_message(msg)
connection = None

class CmdWebSocket(tornado.websocket.WebSocketHandler):
    '''cmd message handler'''

    def on_open(self):
        global connection
        connection = self

    def on_message(self, msg):
        print('[cmd] on message:', msg)
        emitter.cmdReceived.emit(msg)
