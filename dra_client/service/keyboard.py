
import queue

def send_msg(msg):
    '''Send a new keyboard msg to msg queue'''
    print('keyboard.send_msg:', msg)
    messages.put(msg)

def producer():
    '''Rend a new message from msg queue'''
    msg = messages.get()
    print('keyboard.handle:', msg)
    return msg

def consumer(msg):
    print('keyboard.consumer:', msg)
    return []

def reset():
    '''Remove all messages in queue.

    Call this when browser connects to host service'''
    while True:
        try:
            messages.get_nowait()
        except queue.Empty:
            break

messages = queue.Queue()
