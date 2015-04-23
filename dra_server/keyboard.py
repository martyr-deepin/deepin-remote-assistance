
'''Handle keyboard event sent from client side.'''

import json

import tornado.websocket
import pykeyboard

from dra_utils.log import server_log

keyboard = pykeyboard.PyKeyboard()

def handle(msg):
    '''Emulate a KeyboardEvent.

    msg contains keycode, character and press'''
    try:
        event = json.loads(msg)
    except ValueError as e:
        server_log.warn('[keyboard] malformed keyboard event: %s' % msg)
        return

    if event['press']:
        keyboard.press_key(event['character'])
    else:
        keyboard.release_key(event['character'])

def reset_keyboard():
    '''Reset local keyboard before host service is terminated'''
    print('[keyboard] reset keyboard')
    # First press Escape
    keyboard.press_key('Escape')

    # Then Release Escape
    keyboard.release_key('Escape')


class KeyboardWebSocket(tornado.websocket.WebSocketHandler):
    '''Keyboard message handler'''

    def on_message(self, msg):
        print('[keyboard] on message:', msg)
        handle(msg)

    def on_close(self):
        server_log.debug('[keyboard] on close')
        reset_keyboard()
