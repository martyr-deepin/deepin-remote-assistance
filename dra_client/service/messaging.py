
'''Handle messages'''

import json

from dra_utils.log import client_log
from . import constants

# Method to send messages to browser
send_message = lambda *args: print('Unhandled Message: ', args)

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
    print('send keyboard event:', event)
    send_message(constants.KEYBOARD_MSG, event)

def handle_cmd_message(msg):
    '''Handle cmd messages'''
    msg = json.loads(msg)

    if msg['Type'] == constants.CLIENT_MSG_CONNECTED:
        # Change client status to CONNECT_OK
        client_dbus.StatusChanged(constants.CLIENT_STATUS_CONNECT_OK)

def on_main_window_closed():
    '''Change status to CLIENT_STATUS_STOPPED when main window is closed'''
    client_dbus.StatusChanged(constants.CLIENT_STATUS_STOPPED)
