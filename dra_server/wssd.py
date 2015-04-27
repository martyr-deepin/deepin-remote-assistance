
'''
Host websocket service, running in client and server side
'''

from PyQt5 import QtCore
from PyQt5 import QtWidgets
import tornado.ioloop
import tornado.web
import tornado.websocket

from .clipboard import ClipboardWebSocket
from .cmd import CmdWebSocket
from .handshake import HandshakeWebSocket
from .keyboard import KeyboardWebSocket
from .mouse import MouseWebSocket
from dra_utils.log import server_log

# Minimum port to be bound
PORT_MIN = 10000

# Maximum port to be bound
PORT_MAX = 10050


class WSSDWorker(QtCore.QObject):

    browserCmd = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, host='localhost'):
        super().__init__(parent)
        self.host = host
        self.port = PORT_MIN

        # tornado event loop
        self.loop = None

        self.application = tornado.web.Application([
            ('/handshake', HandshakeWebSocket),
            ('/clipboard', ClipboardWebSocket),
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
            # TODO: raise exception
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


class WSSDController(QtCore.QObject):
    '''Controller of WSS Daemon'''

    started = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.workerThread = QtCore.QThread()
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
        QtWidgets.qApp.aboutToQuit.connect(self.stop)
        
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
