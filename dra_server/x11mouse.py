
import json

from pymouse import PyMouse

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
    event['button'] += 1
    return event

def parse(obj):
    event = MouseEvent()
    event.x = obj['x']
    event.y = obj['y']
    event.timeStamp = obj['timeStamp']
    event.button = obj['button'] + 1
    return event

def stringify(event):
    obj = {
        'x': event.x,
        'y': event.y,
        'button': event.button,
        'timeStamp': event.timeStamp,
    }
    return json.dumps(obj)

class MouseEvent(object):

    x = 0
    y = 0
    button = 0
    timeStamp = 0


mouse = PyMouse()
def move(event):
    mouse.move(event['x'], event['y'])

def button_press(event):
    mouse.press(event['x'], event['y'], event['button'])

def button_release(event):
    mouse.release(event['x'], event['y'], event['button'])

def click(event):
    '''Emulate mouse click event.'''
    button_press(event)
    button_release(event)

def handle_mouse_event(ws, msg):
    '''Handle mouse event'''
    print('handle mouse event:', msg)

    # TODO: catch json exception
    event = json.loads(msg)

    # event filter
    event = filter_event_to_local(event)

    handlers = {
        'mousemove': move,
        'mousedown': button_press,
        'mouseup': button_release,
    }
    try:
        handler = handlers[event['type']]
        handler(event)
    except ValueError as e:
        print(e)
        print('TODO: unknown mouse event type,', event)
    return []
