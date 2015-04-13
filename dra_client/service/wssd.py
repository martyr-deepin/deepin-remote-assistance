
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

from . import constants
from . import cmd
from . import default_handler
from . import keyboard
from dra_utils.log import client_log

class WSSDWorker(QObject):

    browserCmd = pyqtSignal(str)

    def __init__(self, parent=None, host='localhost'):
        super().__init__(parent)
        self.host = host
        self.port = constants.PORT_MIN

        self.handlers = {
            '/': default_handler,
            '/mouse': default_handler,
            '/keyboard': keyboard,
            '/clipboard': default_handler,
            '/cmd':  cmd,
            '/handshake': default_handler,
        }

    def start_server(self):
        self.event_loop = asyncio.new_event_loop()
        asyncio.events.set_event_loop(self.event_loop)
        for port in range(constants.PORT_MIN, constants.PORT_MAX):
            try:
                server = websockets.serve(self._handler, self.host, port)
                self.event_loop.run_until_complete(server)
                self.port = port
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
        handler = self.handlers.get(path, None)
        print('message handler:', ws, path)
        if not handler:
            print('TODO: handle this event')
            return

        # TODO: move this to another module
        #if path == '/keyboard':
            #keyboard.reset()

        # FIXME: unblock this handler
        while True:
            # Receive cmd messages from browser
            # cmd connection is bidirectional
            msg = yield from ws.recv()
            if msg is not None:
                yield from handler.consumer(msg)

            # Send message to browser
            if not ws.open:
                client_log.info('websocket of %s is closed' % path)
                break
            msg = yield from handler.producer()
            print('producer.msg:', msg)
            if not msg:
                yield from asyncio.sleep(1)
                continue
            client_log.debug('will send message: %s' % msg)
            try:
                yield from ws.send(msg)
            except websockets.exceptions.InvalidState as e:
                client_log.warn('Error: ws.send(msg): %s' % e)
                break

    def stop_server(self):
        print('worker stop')
        self.event_loop.close()

    def handle_cmd_event(self, ws, msg):
        '''Handle browser command event in UI thread'''
        print('wssd.handle_cmd_event:', ws, msg)
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
            self.workerThread.quit()
            self.workerThread.wait(1)
