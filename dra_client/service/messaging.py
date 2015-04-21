
'''Handle messages'''

import json

from PyQt5 import QtCore

from dra_utils.log import client_log
from . import constants

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
        try:
            video_property = json.loads(msg['Payload'])
        except ValueError as e:
            client_log.warn('[messaging] Failed to read video info: %s, %s' %
                    (e, msg['Payload']))
            return

        client_dbus.engine.window.setVideoAspectRatio(
            video_property['width'], video_property['height'])
    elif msg['Type'] == constants.CLIENT_MSG_UNAVAILABLE:
        client_dbus.StatusChanged(constants.CLIENT_STATUS_UNAVAILABLE)
    elif msg['Type'] == constants.CLIENT_MSG_DISCONNECTED:
        client_dbus.StatusChanged(constants.CLIENT_STATUS_DISCONNECTED)
        # Kill host service after 1s
        QtCore.singleShot(1000, client_dbus.Stop)
    else:
        lient_log.warn('[messaging] Warning: handle this message: %s' % msg)
