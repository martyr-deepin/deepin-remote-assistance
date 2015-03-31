
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
    if 'button' in event:
        event['button'] += 1

mouse = PyMouse()
def move(event):
    mouse.move(event['clientX'], event['clientY'])

def button_press(event):
    mouse.press(event['clientX'], event['clientY'], event['button'])

def button_release(event):
    mouse.release(event['clientX'], event['clientY'], event['button'])

def click(event):
    '''Emulate mouse click event.'''
    button_press(event)
    button_release(event)

def scroll(event):
    # TODO: convert scroll event to middle-up/middle-down event
    mouse.scroll(vertical=event['deltaY'], horizontal=event['deltaX'])

def handle(ws, msg):
    '''Handle mouse event'''
    print('handle mouse event:', msg)

    # TODO: catch json exception
    event = json.loads(msg)

    # event filter
    filter_event_to_local(event)

    handlers = {
        'mousemove': move,
        'mousedown': button_press,
        'mouseup': button_release,
        'wheel': scroll,
    }
    try:
        handler = handlers[event['type']]
        handler(event)
    except ValueError as e:
        print(e)
        print('TODO: unknown mouse event type,', event)
    return []
