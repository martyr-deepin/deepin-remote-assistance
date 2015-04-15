
'''
Host websocket service, running in client and server side
'''

import asyncio

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import qApp
import websockets

#from . import cmd
from . import handshake
from . import mouse
from . import keyboard
from dra_utils.log import server_log

# Minimum port to be bound
PORT_MIN = 10000

# Maximum port to be bound
PORT_MAX = 10050

def default_handler(ws, msg):
    server_log.debug('[wssd] default handler: TODO, %s' % msg)
    return ws.send(msg)

class WSSDWorker(QObject):

    browserCmd = pyqtSignal(str)

    def __init__(self, parent=None, host='localhost'):
        super().__init__(parent)
        self.host = host
        self.port = PORT_MIN

        self.handlers = {
            '/': default_handler,
            '/mouse': mouse.handle,
            '/keyboard': keyboard.handle,
            '/clipboard': default_handler,
            '/cmd':  self.handle_cmd_event,
            '/handshake': handshake.handle,
        }

    def start_server(self):
        self.event_loop = asyncio.new_event_loop()
        asyncio.events.set_event_loop(self.event_loop)
        for port in range(PORT_MIN, PORT_MAX):
            try:
                server = websockets.serve(self._handler, self.host, port)
                self.event_loop.run_until_complete(server)
                self.port = port
                break
            except OSError as e:
                server_log.warn('[wssd] %s' % e)
                print(e)

        # FIXME: AttributeError
        try:
            self.event_loop.run_forever()
        except AttributeError as e:
            server_log.warn('[wssd] %s' % e)
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
                server_log.debug('[wssd] TODO: handle this event: %s' % path)
                continue
            yield from handler(ws, msg)

    def stop_server(self):
        server_log.info('[wssd] worker stop')
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
        server_log.info('[wssd] controller stopped')
        if self.worker_started:
            self.worker.stop_server()
        if not self.workerThread.isFinished():
            self.workerThread.quit()
            self.workerThread.wait(1)
