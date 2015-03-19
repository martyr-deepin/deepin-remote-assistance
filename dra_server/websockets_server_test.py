#!/usr/bin/env python3

import asyncio
import json

import websockets


def consumer(websocket, message):
    print('consumer:', message)
    result = websocket.send(message)
    print('result:', result)
    return result

def noop(websocket, message):
    print('noop:', websocket, message)
    result = websocket.send(message)
    return result

def double_echo(websocket, message):
    return websocket.send(message * 2)

@asyncio.coroutine
def handler(websocket, path):
    handlers = {
        '/': noop,
        '/one': consumer,
        '/two': double_echo,
    }
    while True:
        message = yield from websocket.recv()
        if message is None:
            break
        handler = handlers[path]
        yield from handler(websocket, message)


port = 9001
print('Listenering on :9001')
subprotocols = ['deepin']
start_server = websockets.serve(handler, 'localhost', port,
        subprotocols=subprotocols)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
