
'''Send cmd messages'''

import json
import queue

from . import constants


messages = queue.Queue()

def send_msg(msg):
    print('will send cmd message:', msg)
    messages.put(msg)

def handle():
    msg = messages.get()
    print('cmd.handle:', msg)
    return msg

def reset():
    while True:
        try:
            messages.get_nowait()
        except queue.Empty:
            break

# Send sepcific cmd messages to browser side
def init_remoting(remote_peer_id):
    '''Setup a new remoting connection'''
    msg = json.dumps({
        'Type': constants.CLIENT_MSG_INIT,
        'Pyaload': remote_peer_id,
    })
    send_msg(msg)

