
import subprocess
import threading
import time

from Xlib import display
import Xlib.error

from . import ewmh

# 20 milliseconds
INTERVAL = 20.0 / 1000.0

# Maximum retries
MAX_TRY = 1000

dpy = display.Display()
manager = ewmh.EWMH()

def launch_app_in_background(args, shell=False):
    '''Launch a GUI application in background and hide its window'''

    def hide_window(pid):
        '''Hide window with specific pid'''

        count = 0
        found_client = False

        while True:
            for client in manager.getClientList():
                try:
                    client_pid = manager.getWmPid(client)
                    if client_pid == pid:
                        found_client = True
                        print('unmap now:', client, client.id)
                        client.unmap_sub_windows()
                        status = client.unmap()
                        dpy.flush()
                except (TypeError, Xlib.error.BadWindow):
                    continue

            if count >= MAX_TRY and found_client:
                return
            time.sleep(INTERVAL)
            count += 1

    popen = subprocess.Popen(args, shell=shell)
    t = threading.Thread(target=hide_window, args=[popen.pid,])
    t.daemon = True
    t.start()
    return popen
