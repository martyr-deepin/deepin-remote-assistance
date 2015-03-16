#!/usr/bin/env python3

import asyncio

import websockets

@asyncio.coroutine
def hello():
    msg = 'hello'
    #ws = yield from websockets.connect('ws://localhost:9001/one')
    ws = yield from websockets.connect('ws://localhost:9001/two')
    print('> ', msg)
    yield from ws.send(msg)
    result = yield from ws.recv()
    print('< ', result)
asyncio.get_event_loop().run_until_complete(hello())
