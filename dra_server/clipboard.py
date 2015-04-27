
import json

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import tornado.websocket

from dra_utils.log import server_log
from . import constants

def init(server_dbus):
    global clipboard_daemon
    clipboard_daemon = ClipboardDaemon()

def send_message(msg):
    '''Send clipboard data to browser'''
    if not connection:
        server_log.debug('[clipboard] connection is uninitialized')
        return
    connection.write_message(msg)


@QtCore.pyqtSlot(str)
def handle(msg):
    '''Handle clipboard data messages'''
    try:
        msg = json.loads(msg)
    except ValueError as e:
        server_log.warn('[clipboard] Warning: handle this error: %s' % e)
        return

    print('[clipboard] msg:', msg)
    if msg['type'] == constants.CLIPBOARD_TEXT:
        clipboard_daemon.set_text(msg['payload'])
    elif msg['type'] == constants.CLIPBOARD_PIXMAP:
        clipboard_daemon.set_pixmap(msg['payload'])
    else:
        server_log.warn('[clipboard] unsupported clipboard data %s.' % msg)

class Emitter(QtCore.QObject):
    '''Emitter class is used to send msgReceived signal.

    That signal shall be handled in UI thread'''

    msgReceived = QtCore.pyqtSignal(str)
    
emitter = Emitter()
emitter.msgReceived.connect(handle)

# This object is used to send message to browser
# CGeck connection and call connection.write_message(msg)
connection = None

class ClipboardWebSocket(tornado.websocket.WebSocketHandler):
    '''clipboard message handler'''

    def open(self):
        print('[clipboard] on open')
        global connection
        connection = self

    def on_message(self, msg):
        print('[clipboard] on message:', msg)
        emitter.msgReceived.emit(msg)

class ClipboardDaemon(QtCore.QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Get system clipboard
        self.clipboard = QtWidgets.qApp.clipboard()
        # TODO: check self.clipboard is not None
        if self.clipboard:
            self.clipboard.dataChanged.connect(self.onClipboardDataChanged)
        else:
            print('[clipboard] warning:', self.clipboard, 'is None')
            server_log.warn('[clipboard] failed to init clipboard')

    def onClipboardDataChanged(self):
        # If connection not initialized, ignore current clipboard content
        print('[clipboard] on data changed')
        if not connection:
            return
        text = self.clipboard.text(QtGui.QClipboard.Clipboard)
        pixmap = self.clipboard.pixmap(QtGui.QClipboard.Clipboard)
        # Check text first
        if text:
            msg = {
                'type': constants.CLIPBOARD_TEXT,
                'payload': text,
            }
            send_message(json.dumps(msg))
        elif pixmap:
            msg = {
                'type': constants.CLIPBOARD_PIXMAP,
                'payload': pixmap,
            }
            print('TODO: [clipboard] serialize pixmap:', pixmap)
        else:
            server_log.warn('[clipboard] unknown clipboard data')

    def set_text(self, text):
        '''Update text content of global clipboard'''
        print('[clipboard] set text:', text)
        self.clipboard.dataChanged.disconnect(self.onClipboardDataChanged)
        self.clipboard.setText(text, QtGui.QClipboard.Clipboard)
        self.clipboard.dataChanged.connect(self.onClipboardDataChanged)

    def set_pixmap(self, pixmap):
        '''Update pixmap of global clipboard'''
        pass
        #self.clipboard.dataChanged.disconnect(self.onClipboardDataChanged)
        #self.clipboard.setPixmap(pixmap, QtGui.QClipboard.Clipboard)
        #self.clipboard.dataChanged.connect(self.onClipboardDataChanged)

clipboard_daemon = None
