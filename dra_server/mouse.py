
import json

from pymouse import PyMouse
import Xlib
import Xlib.display
import tornado.websocket

from dra_utils.log import server_log

def filter_event_to_local(event):
    '''Properties of MouseEvent in browsers are slitely different from
        those in X11.

    In browsers:
      0 -> left
      1 -> middle
      2 -> right

    In X Server:
      1 -> left
      2 -> middle
      3 -> right
      4 -> middle up
      5 -> middle down
    '''
    if 'button' in event:
        event['button'] += 1

    # Remap mouse position
    # localX / localWidth = remoteOffsetX / remoteVideoWidth
    event['localX'] = int(event['offsetX'] * screen_width / event['w'])
    event['localY'] = int(event['offsetY'] * screen_height / event['h'])
    return event

def get_screen_resolution():
    '''Get current resolution of default screen'''
    resolution = Xlib.display.Display().screen().root.get_geometry()
    return (resolution.width, resolution.height)

mouse = PyMouse()
screen_width, screen_height = get_screen_resolution()

def move(event):
    mouse.move(event['localX'], event['localY'])

def button_press(event):
    print('button press:', event)
    mouse.press(event['localX'], event['localY'], event['button'])

def button_release(event):
    print('button release:', event)
    mouse.release(event['localX'], event['localX'], event['button'])

def click(event):
    '''Emulate mouse click event.'''
    button_press(event)
    button_release(event)

def scroll(event):
    # TODO: convert scroll event to middle-up/middle-down event
    mouse.scroll(vertical=event['deltaY'], horizontal=event['deltaX'])

def handle(msg):
    '''Handle mouse event'''
    print('handle mouse event:', msg)

    # TODO: catch json exception
    event = json.loads(msg)

    # event filter
    event = filter_event_to_local(event)

    handlers = {
        'move': move,
        'press': button_press,
        'release': button_release,
        # TODO: handle mouse scrolling event
        #'wheel': scroll,
    }
    try:
        handler = handlers[event['type']]
        handler(event)
    except ValueError as e:
        print(e)
        print('TODO: unknown mouse event type,', event)
    return []


class MouseWebSocket(tornado.websocket.WebSocketHandler):
    '''mouse message handler'''

    def on_message(self, msg):
        print('[mouse] on message:', msg)
        handle(msg)

    def on_close(self):
        print('[mouse] on close')
        # TODO: release any mouse event')
