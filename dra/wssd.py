
'''
Host websocket service, running in client and server side
'''

import asyncio
import json
import multiprocessing
import threading

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import websockets

from dra.command import handle_cmd_event
from dra.handshake import handle_handshake_event
from dra.x11mouse import handle_mouse_event
from dra.x11keyboard import handle_keyboard_event

# Minimum port to be bound
PORT_MIN = 10000

# Maximum port to be bound
PORT_MAX = 10050

def default_handler(ws, msg):
    print('TODO:', msg)
    return ws.send(msg)

class WSSDWorker(QObject):

    browserCmd = pyqtSignal(str)

    def __init__(self, parent=None, host='localhost'):
        super().__init__(parent)
        self.host = host
        self.port = PORT_MIN

        self.handlers = {
            '/': default_handler,
            '/mouse': handle_mouse_event,
            '/keyboard': handle_keyboard_event,
            '/clipboard': default_handler,
            '/cmd':  self.handle_cmd_event,
            '/handshake': handle_handshake_event,
        }

    def start_server(self):
        self.event_loop = asyncio.new_event_loop()
        for port in range(PORT_MIN, PORT_MAX):
            try:
                server = websockets.serve(self._handler, self.host, port)
                self.event_loop.run_until_complete(server)
                self.port = port
                print('selected port:', port, self.port)
                break
            except OSError as e:
                print(e)

        self.event_loop.run_forever()

    @asyncio.coroutine
    def _handler(self, ws, path):
        while True:
            msg = yield from ws.recv()
            if msg is None:
                break
            # TODO: catch KeyError exception
            handler = self.handlers[path]
            yield from handler(ws, msg)

    def stop_server(self):
        # FIXME:
        #del self
        pass

    def handle_cmd_event(self, ws, msg):
        self.browserCmd.emit(msg)

    def __str__(self):
        return 'WSSDWorker<%s:%s>' % (self.host, self.port)

    def __repr__(self):
        return self.__str__()

class WSSDWorkerThread(QThread):
    
    def __init__(self):
        super().__init__()

    def run(self):
        asyncio.get_event_loop().run_forever()


class WSSDController(QObject):
    '''Controller of WSS Daemon'''

    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.worker = WSSDWorker(self)
        #self.workerThread = QThread()
        self.workerThread = WSSDWorkerThread()
        # The object cannot be moved if it has a parent.
        # See http://doc.qt.io/qt-5/qobject.html#moveToThread
        #self.worker.moveToThread(self.workerThread)
        self.started.connect(self.worker.start_server)
        self.stopped.connect(self.worker.stop_server)

        #self.workerThread.start()
        
    def start(self):
        self.started.emit()

    def stop(self):
        self.stopped.emit()

# TODO: WSSD heritated from QObject
# TODO: WSSD -> threading.Thread
# TODO: move this class to a new process
class WSSD():

    handlers = {
        '/': default_handler,
        '/mouse': handle_mouse_event,
        '/keyboard': handle_keyboard_event,
        '/clipboard': default_handler,
        '/cmd':  handle_cmd_event,
        '/handshake': handle_handshake_event,
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
