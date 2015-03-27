
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

    event = json.loads(msg)
    if event['press']:
        keyboard.press_key(event['character'])
    else:
        keyboard.release_key(event['character'])
    return []
