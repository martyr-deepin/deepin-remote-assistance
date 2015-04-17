
'''Handle keyboard event sent from client side.'''

import json

import Xlib.display
import Xlib.ext.xtest as xtest
import Xlib.X as X
import Xlib.XK
local_display = Xlib.display.Display()

import pykeyboard
keyboard = pykeyboard.PyKeyboard()


def handle(ws, msg):
    '''Message is a KeyboardEvent, including keycode, character, press'''
    print('handle:', msg)

    # TODO: catch json exception
    try:
        event = json.loads(msg)
    except ValueError as e:
        server_log.warn('[keyboard] %s malformed keyboard event: %s' %
                        (e, msg))
        return

    if event['press']:
        keyboard.press_key(event['character'])
    else:
        keyboard.release_key(event['character'])
    return []
