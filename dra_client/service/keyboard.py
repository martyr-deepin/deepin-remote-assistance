
#import asyncio
#import threading
import queue

# WebSocket connection for keyboard event
#keyboard_conn = None
#
#def bind_keyboard_conn(ws, msg):
#    print('bind keyboard conn')
#    global keyboard_conn
#    keyboard_conn = ws
#    return ws.send(msg)

#def send_event(event):
#    print('send event:', keyboard_conn, event)
#    if keyboard_conn:
#        keyboard_conn.send(event)
#    else:
#        print('keyboard connection uninitialized!')


#class KeyboardReader(asyncio.StreamReaderProtocol):
#
#    def __init__(self, loop=None):
#        stream_reader = asyncio.StreamReader(loop=loop)
#        super().__init__(stream_reader, loop=loop)
#
#        self.messages = asyncio.Queue()
#
#        # Task managing the connection.
#        self.worker = asyncio.async(self.run(), loop=loop)
#
#    @asyncio.coroutine
#    def run(self):
#        pass
#
#    @asyncio.coroutine
#    def recv(self):
#        print('recv():')
#        # Return any available message
#        try:
#            return self.messages.get_nowait()
#        except asyncio.QueueEmpty:
#            pass
#
#        # Wait for a message until the connection is closed
#        next_message = asyncio.async(self.messages.get(), loop=self._loop)
#        print('next message:', next_message)
#        done, pending = yield from asyncio.wait(
#                [next_message, ],
#                loop=self._loop, return_when=asyncio.FIRST_COMPLETED)
#        print('done:', done)
#        print('pending:', pending)
#        if next_message in done:
#            return next_message.result()
#        else:
#            next_message.cancel()
#        print('returns None')
#
#def send_event(event):
#    print('send event:', event)
#    reader.messages.put(event)

#reader = KeyboardReader()

def send_event(event):
    events.put(event)

def handler():
    event = events.get()
    return event

#@asyncio.coroutine
#def handler():
#    try:
#        events = queue.get_nowait()
#        print('events:', events)
#        return events
#    except asyncio.QueueEmpty:
#        pass
#
#    task = asyncio.async(queue.get(), loop=loop)
#    print('task:', task)
#    done, pending = yield from asyncio.wait([task,], loop=loop)
#    print('done:', done)
#    print('pending:', pending)
#
#queue = asyncio.Queue()
#loop = asyncio.new_event_loop()
#loop.run_forever()
#thread = threading.Thread(target=loop.run_forever)
#thread.start()

events = queue.Queue()
