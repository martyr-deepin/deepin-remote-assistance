#!/usr/bin/env python3

import sys
sys.path.insert(0, '..')

from PyQt5 import QtCore

from dra_server.server_dbus import ServerDBus
from dra_utils.log import server_log

def main():
    server_dbus = ServerDBus()
    # FIXME: log service failed to dump log
    server_log.debug('Init server dbus: %s' % server_dbus)
    app = QtCore.QCoreApplication(sys.argv)
    app.exec()

if __name__ == '__main__':
    main()
