
'''
Host websocket service, running in client and server side
'''

import asyncio

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import qApp
import tornado.ioloop
import tornado.web
import tornado.websocket

from .cmd import CmdWebSocket
from .handshake import HandshakeWebSocket
from .keyboard import KeyboardWebSocket
from .mouse import MouseWebSocket
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

        # tornado event loop
        self.loop = None

        self.application = tornado.web.Application([
            ('/handshake', HandshakeWebSocket),
            ('/cmd', CmdWebSocket),
            ('/mouse', MouseWebSocket),
            ('/keyboard', KeyboardWebSocket),
        ])

    def start_server(self):
        for port in range(PORT_MIN, PORT_MAX):
            try:
                self.application.listen(port)
                break
            # That port is unavailable
            except OSError:
                pass
        else:
            server_log.warn('[wssd] failed to start websocket server')
            return

        self.port = port
        self.loop = tornado.ioloop.IOLoop.instance()
        self.loop.start()

    def stop_server(self):
        server_log.info('[wssd] worker stop')
        if self.loop:
            self.loop.stop()

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
