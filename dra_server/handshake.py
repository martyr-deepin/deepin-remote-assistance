

from dra_utils import ByPassOriginWebSocketHandler

class HandshakeWebSocket(ByPassOriginWebSocketHandler):

    def on_message(self, msg):
        print('[handhshake] on message:', msg)
        self.write_message(msg)
