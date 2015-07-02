
import json

from PyQt5 import QtCore

from dra_utils.log import server_log
from dra_utils import ByPassOriginWebSocketHandler
from . import constants

def init(server_dbus_):
    '''Init server_dbus instance'''
    global server_dbus
    server_dbus = server_dbus_

server_dbus = None

@QtCore.pyqtSlot(str)
def handle(msg):
    '''Handle command message sent from browser side.

    Some of these messages will be converted to Qt mssage'''
    server_log.debug('[cmd] handle: %s' % msg)
    if not server_dbus:
        server_log.warn('[cmd] server_dubs not inited yet')
        print('[cmd] server dubs not inited yet:', server_dbus)
        return
    try:
        msg = json.loads(msg)
    except ValueError as e:
        server_log.warn('[cmd] failed to parse msg')
        return

    if msg['Type'] == constants.SERVER_MSG_ECHO:
        server_dbus.peer_id_changed(msg['Payload'])
    elif msg['Type'] == constants.SERVER_MSG_SHARING:
        server_dbus.StatusChanged(constants.SERVER_STATUS_SHARING)
    elif msg['Type'] == constants.SERVER_MSG_DISCONNECT:
        server_dbus.StatusChanged(constants.SERVER_STATUS_DISCONNECTED)
    elif msg['Type'] == constants.SERVER_MSG_WEBRTC_FAILED:
        # TODO: add SERVER_STATUS_WEBRTC_FAILED status
        server_dbus.StatusChanged(constants.SERVER_STATUS_DISCONNECTED)
    else:
        server_log.warn('handleBrowserCmd msg invalid: %s' % msg)

class Emitter(QtCore.QObject):
    '''Emitter class is used to send cmdReceived signal.

    That signal shall be handled in UI thread'''

    cmdReceived = QtCore.pyqtSignal(str)
    
emitter = Emitter()
emitter.cmdReceived.connect(handle)


class CmdWebSocket(ByPassOriginWebSocketHandler):
    '''cmd message handler'''

    def on_message(self, msg):
        print('[cmd] on message:', msg)
        emitter.cmdReceived.emit(msg)
