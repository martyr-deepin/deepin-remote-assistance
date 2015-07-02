
'''Handle keyboard event sent from client side.'''

import json

from Xlib import X
from Xlib.display import Display
from Xlib.ext.xtest import fake_input

from dra_utils import ByPassOriginWebSocketHandler
from dra_utils.log import server_log

dp = Display()

# keycode of Escape key
ESCAPE_CODE = 9

def press_key(code):
    fake_input(dp, X.KeyPress, code)
    dp.sync()

def release_key(code):
    fake_input(dp, X.KeyRelease, code)
    dp.sync()

def reset_keyboard():
    '''Reset local keyboard before host service is terminated'''
    print('[keyboard] reset keyboard')
    # First press Escape
    press_key(ESCAPE_CODE)

    # Then Release Escape
    release_key(ESCAPE_CODE)

def handle(msg):
    '''Emulate a KeyboardEvent.

    msg contains keycode, character and press'''
    try:
        event = json.loads(msg)
    except ValueError as e:
        server_log.warn('[keyboard] malformed keyboard event: %s' % msg)
        return

    if event['press']:
        press_key(event['code'])
    else:
        release_key(event['code'])


class KeyboardWebSocket(ByPassOriginWebSocketHandler):
    '''Keyboard message handler'''

    def on_message(self, msg):
        print('[keyboard] on message:', msg)
        handle(msg)

    def on_close(self):
        server_log.debug('[keyboard] on close')
        reset_keyboard()
