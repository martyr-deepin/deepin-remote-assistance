#!/usr/bin/env python3

import sys

from PyQt5 import QtGui

from dra_client.service.client_dbus import ClientDBus
from dra_utils.log import client_log

def main():
    client_dbus = ClientDBus()
    # FIXME: log service failed to dump log
    client_log.debug('Init client dbus: %s' % client_dbus)

    app = QtGui.QGuiApplication(sys.argv)
    app.exec()

if __name__ == '__main__':
    main()
