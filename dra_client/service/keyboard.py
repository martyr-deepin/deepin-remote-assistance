

# WebSocket connection for keyboard event
keyboard_conn = None

def bind_keyboard_conn(ws, msg):
    global keyboard_conn
    keyboard_conn = ws
    return ws.send(msg)

def send_event(event):
    if keyboard_conn:
        keyboard_conn.send(event)
    else:
        print('keyboard connection uninitialized!')
