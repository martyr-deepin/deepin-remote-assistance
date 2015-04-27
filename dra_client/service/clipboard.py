
import json

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import tornado.websocket

from dra_utils.log import client_log
from . import constants

def init(client_dbus):
    global clipboard_daemon
    clipboard_daemon = ClipboardDaemon()

def send_message(msg):
    '''Send clipboard data to browser'''
    if not connection:
        client_log.debug('[clipboard] connection is uninitialized')
        return
    print('[clipboard] send message:', msg)
    connection.write_message(msg)


@QtCore.pyqtSlot(str)
def handle(msg):
    '''Handle clipboard data messages'''
    try:
        msg = json.loads(msg)
    except ValueError as e:
        client_log.warn('[clipboard] Warning: handle this error: %s' % e)
        return
    if msg['type'] == constants.CLIPBOARD_TEXT:
        clipboard_daemon.set_text(msg['payload'])
    elif msg['type'] == constants.CLIPBOARD_PIXMAP:
        clipboard_daemon.set_pixmap(msg['payload'])
    else:
        client_log.warn('[clipboard] unsupported clipboard data %s.' % msg)

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
        handle(msg)

class ClipboardDaemon(QtCore.QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Get system clipboard
        self.clipboard = QtWidgets.qApp.clipboard()

        self.clipboard.dataChanged.connect(self.onClipboardDataChanged)

    def onClipboardDataChanged(self):
        # If connection not initialized, ignore current clipboard content
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
            client_log.warn('[clipboard] unknown clipboard data')

    def set_text(self, text):
        '''Update text content of global clipboard'''
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
