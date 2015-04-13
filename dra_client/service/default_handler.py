
import asyncio

@asyncio.coroutine
def consumer(msg):
    print('default consumer:', msg)
    return []

@asyncio.coroutine
def producer():
    print('default producer')
    return []
