
'''
Host websocket service, running in client and server side
'''

import asyncio
import json

import websockets

PORT_MIN = 30000
PORT_MAX = 30050

class EventTypes(object):
    KEYBOARD = 0
    MOUSE = 1
    CLIPBOARD = 2
    CMD = 3
    HANDSHAKE = 4

# Do nothing
noop = lambda *args, **kwgs: pass

def handshake(message):
    '''Send message back to wss client'''
    pass

# TODO: WSSD heritated from QObject
class WSSD:

    handlers = {
        noop,
        noop,
        noop,
        noop,
        handshake,
    )

    def __init__(self):
        pass

    def start(self):
        for port in range(PORT_MIN, PORT_MAX):
            try:
                start_server = websockets.serve(self.handler,
                        'localhost', port)
            except 

        asyncio.get_event_loop().run_until_complete(start_server)
        #asyncio.get_event_loop().run_forever()
        # self.exec()

    def stop(self):
        pass

    def handle_event(self, event):
        '''Event handler router'''

        try:
            self.handlers[event['eventType']](event)
        except IndexError as e:
            print(e)

    def consumer(self, message):
        #print('consumer():', message)
        try:
            event = json.loads(message)
            handle_event(event)
        except ValueError as e:
            print('No appropriate event handler:', e)

        return []

    @asyncio.coroutine
    def handler(self, websocket, path):
    # TODO: use `path` argument
        while True:
            message = yield from websocket.recv()
            if message is None:
                break
            yield from consumer(message)
