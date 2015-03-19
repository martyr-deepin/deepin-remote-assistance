
import json

import Xlib.display
import Xlib.ext.xtest as xtest
import Xlib.X as X
import Xlib.XK
local_display = Xlib.display.Display()

#from pykeyboard import PyKeyboard
#keyboard = PyKeyboard()

def keydown(event):
    pass

def keyup(event):
    pass

def keypress(event):
    '''Emulate key press event.
    
    Order of key press event is:
      onkeydown -> onkeypress -> onkeyup
    '''
    # TODO: handle keyboard modifier (Shift, Ctrl, Alt)
    # TODO: handle repeated keypress event
    keycode = local_display.keysym_to_keycode(event['keyCode'])
    key = Xlib.XK.keysym_to_string(event['keyCode'])
    #print('key:', key)
    xtest.fake_input(local_display, X.KeyPress, keycode)
    xtest.fake_input(local_display, X.KeyRelease, keycode)
    local_display.flush()
    #local_display.sync()

def handle_keyboard_event(ws, msg):

    event = json.loads(msg)

    handlers = {
        'keydown': keydown,
        'keypress': keypress,
        'keyup': keyup,
    }
    try:
        handler = handlers[event['type']]
        handler(event)
    except ValueError as e:
        print(e)
        print('TODO: unknown mouse event type,', event)
    return []
