
import json

from pymouse import PyMouse
import Xlib
import Xlib.X
import Xlib.display
import tornado.websocket

from dra_utils.log import server_log

def filter_event_to_local(event):
    '''Recalculate cursor position'''
    # localX / localWidth = remoteOffsetX / remoteVideoWidth
    event['localX'] = int(event['x'] * screen_width / event['w'])
    event['localY'] = int(event['y'] * screen_height / event['h'])
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
    mouse.press(event['localX'], event['localY'], button=event['button'])

def button_release(event):
    mouse.release(event['localX'], event['localY'], button=event['button'])

#def click(event):
#    '''Emulate mouse click event.'''
#    button_press(event)
#    button_release(event)
#
#def scroll(event):
#    # TODO: convert scroll event to middle-up/middle-down event
#    mouse.scroll(vertical=event['deltaY'], horizontal=event['deltaX'])

# Mouse event handlers
handlers = {
    Xlib.X.MotionNotify: move,
    Xlib.X.ButtonPress: button_press,
    Xlib.X.ButtonRelease: button_release,
}

def handle(msg):
    '''Handle mouse event'''

    # TODO: catch json exception
    event = json.loads(msg)

    # event filter
    event = filter_event_to_local(event)

    try:
        handler = handlers[event['type']]
        handler(event)
    except (KeyError, ValueError) as e:
        print(e)
        print('TODO: unknown mouse event type,', event)


class MouseWebSocket(tornado.websocket.WebSocketHandler):
    '''mouse message handler'''

    def on_message(self, msg):
        print('[mouse] on message:', msg)
        handle(msg)

    def on_close(self):
        print('[mouse] on close')
        # TODO: release any mouse event')
