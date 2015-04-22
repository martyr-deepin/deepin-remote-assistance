
import tornado.websocket

from dra_utils.log import server_log

class HandshakeWebSocket(tornado.websocket.WebSocketHandler):

    def on_message(self, msg):
        print('[handhshake] on message:', msg)
        self.write_message(msg)
