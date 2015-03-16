
'''
Host websocket service, running in client and server side
'''

import asyncio
import json
import multiprocessing

import websockets

from dra.command import handle_cmd_event
from dra.x11mouse import handle_mouse_event
from dra.x11keyboard import handle_keyboard_event

# Minimum port to be bound
PORT_MIN = 10000

# Maximum port to be bound
PORT_MAX = 10050

def default_handler(ws, msg):
    print('TODO:', msg)
    return ws.send(msg)

def handshake(ws, msg):
    '''Send message back to wss client'''
    return ws.send(msg)

# TODO: WSSD heritated from QObject
# TODO: WSSD -> threading.Thread
# TODO: move this class to a new process
class WSSD(multiprocessing.Process):

    handlers = {
        '/': default_handler,
        '/mouse': handle_mouse_event,
        '/keyboard': handle_keyboard_event,
        '/clipboard': default_handler,
        '/cmd':  handle_cmd_event,
        '/handshake': handshake,
    }

    def __init__(self, host='localhost'):
        super().__init__()
        self.host = host
        self.port = 0

    def __str__(self):
        return 'WSSD<%s:%s>' % (self.host, self.port)

    def __repr__(self):
        return self.__str__()
    
    def run(self):
        self._start_server()

    def _start_server(self):
        for port in range(PORT_MIN, PORT_MAX):
            try:
                server = websockets.serve(self._handler, self.host, port)
                asyncio.get_event_loop().run_until_complete(server)
                self.port = port
                print('selected port:', port, self.port)
                break
            except OSError as e:
                print(e)

        print(self)
        asyncio.get_event_loop().run_forever()

    @asyncio.coroutine
    def _handler(self, ws, path):
        while True:
            msg = yield from ws.recv()
            if msg is None:
                break
            # TODO: catch KeyError exception
            handler = self.handlers[path]
            yield from handler(ws, msg)
