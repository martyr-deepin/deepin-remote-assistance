

from dra_utils import ByPassOriginWebSocketHandler
from dra_utils.log import client_log

class HandshakeWebSocket(ByPassOriginWebSocketHandler):

    def on_message(self, msg):
        print('[handhshake] on message:', msg)
        self.write_message(msg)
