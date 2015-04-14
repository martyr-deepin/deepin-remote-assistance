
'''Handle messages'''

import json

from dra_utils.log import client_log
from . import constants

# Method to send messages to browser
send_message = lambda *args: print('Unhandled Message: ', args)

# Reference to client dbus object
client_dbus = None

def init_send_message(sendMessage, clientDBus):
    print('init send message:', sendMessage)
    client_log.debug('init send_message: %s' % sendMessage)
    global send_message
    send_message = sendMessage
    global client_dbus
    client_dbus = clientDBus

def init_remoting(remote_peer_id):
    '''Connect to remote peer'''
    print('init remoting:', remote_peer_id)
    client_log.debug('init_remoting: %s' % remote_peer_id)
    send_message(constants.CMD_MSG, json.dumps({
        'Type': constants.CLIENT_MSG_INIT,
        'Payload': remote_peer_id,
    }))

def send_keyboard_event(event):
    client_log.debug('send_keyboard_event: %s' % event)
    send_message(constants.KEYBOARD_MSG, event)

def handle_cmd_message(msg):
    '''Handle cmd messages'''
    msg = json.loads(msg)

    if msg['Type'] == constants.CLIENT_MSG_CONNECTED:
        client_dbus.change_client_status(constants.CLIENT_STATUS_CONNECT_OK)
