
import subprocess
import threading
import time

from Xlib import display

import ewmh

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
        print('hide window:', pid)

        count = 0
        found_client = False

        while True:
            for client in manager.getClientList():
                try:
                    client_pid = manager.getWmPid(client)
                    #print('client_pid:', client_pid)
                    if client_pid == pid:
                        found_client = True
                        print('unmap now:', client, client.id)
                        client.unmap_sub_windows()
                        status = client.unmap()
                        dpy.flush()
                except TypeError:
                    continue

            if count >= MAX_TRY and found_client:
                print('will return now')
                return
            print('sleep now')
            time.sleep(INTERVAL)
            count += 1

    popen = subprocess.Popen(args, shell=shell)
    t = threading.Thread(target=hide_window, args=[popen.pid,])
    t.daemon = True
    t.start()
    return popen
