#!/usr/bin/env python3

import sys

from PyQt5 import QtWidgets

from dra_client.service.client_dbus import is_client_dbus_running
from dra_client.service.client_dbus import ClientDBus
from dra_server.server_dbus import is_server_dbus_running
from dra_utils.constants import APP_NAME
from dra_utils.log import client_log

def main():
    if is_client_dbus_running():
        client_log.warn('[client] client side is running')
        return
    if is_server_dbus_running():
        client_log.warn('[client] server side is running')
        return
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    client_dbus = ClientDBus()
    # FIXME: log service failed to dump log
    client_log.debug('Init client dbus: %s' % client_dbus)

    app.exec()

if __name__ == '__main__':
    main()
