
import tornado.websocket

class ByPassOriginWebSocketHandler(tornado.websocket.WebSocketHandler):
    '''Bypass default securitiy policy in tornado(>= 4.0).
    http://tornado.readthedocs.org/en/latest/_modules/tornado/websocket.html 
    '''

    def check_origin(self, origin):
        '''Always returns True'''
        return True
