
import queue

def send_event(event):
    '''Send a new keyboard event to event queue'''
    events.put(event)

def handler():
    '''Rend a new message from event queue'''
    event = events.get()
    return event

def reset():
    '''Remove all events in queue.

    Call this when browser connects to host service'''
    while True:
        try:
            events.get_nowait()
        except queue.Empty:
            break

events = queue.Queue()
