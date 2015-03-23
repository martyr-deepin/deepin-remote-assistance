
'''
Host websocket service, running in client and server side
'''

import asyncio
import json
import threading

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import qApp
import websockets

#from .command import handle_cmd_event
from .handshake import handle_handshake_event
from .x11mouse import handle_mouse_event
from .x11keyboard import handle_keyboard_event

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
        asyncio.events.set_event_loop(self.event_loop)
        for port in range(PORT_MIN, PORT_MAX):
            try:
                server = websockets.serve(self._handler, self.host, port)
                print('server:', server)
                self.event_loop.run_until_complete(server)
                print('loop:', self.event_loop)
                self.port = port
                print('selected port:', port, self.port)
                break
            except OSError as e:
                print(e)

        # FIXME: AttributeError
        try:
            self.event_loop.run_forever()
        except AttributeError as e:
            print(e)

    @asyncio.coroutine
    def _handler(self, ws, path):
        while True:
            msg = yield from ws.recv()
            if msg is None:
                break
            handler = self.handlers.get(path, None)
            if not handler:
                print('TODO: handle this event')
                continue
            yield from handler(ws, msg)

    def stop_server(self):
        print('worker stop')
        self.event_loop.close()

    def handle_cmd_event(self, ws, msg):
        '''Handle browser command event in UI thread'''
        self.browserCmd.emit(msg)
        return []

    def __str__(self):
        return 'WSSDWorker<%s:%s>' % (self.host, self.port)

    def __repr__(self):
        return self.__str__()


class WSSDController(QObject):
    '''Controller of WSS Daemon'''

    started = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.workerThread = QThread()
        self.worker = WSSDWorker()
        # The object cannot be moved if it has a parent.
        # See http://doc.qt.io/qt-5/qobject.html#moveToThread
        self.worker.moveToThread(self.workerThread)
        self.started.connect(self.worker.start_server)

        # Start background thread
        self.workerThread.start()

        # To mark worker running status
        self.worker_started = False

        # Stop worker thread when app is killed
        qApp.aboutToQuit.connect(self.stop)
        
    def start(self):
        if self.worker_started:
            return
        self.worker_started = True
        self.started.emit()

    def stop(self):
        print('controller stop')
        if self.worker_started:
            self.worker.stop_server()
        # FIXME: segmantation fault
        if not self.workerThread.isFinished():
            self.workerThread.exit()
