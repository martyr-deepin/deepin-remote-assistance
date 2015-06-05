#!/usr/bin/env python3

import sys

import dbus
import dbus.service
import dbus.mainloop.glib
from dbus.mainloop.glib import DBusGMainLoop
dbus.mainloop.glib.threads_init()
from PyQt5 import QtCore

from dra_utils import constants
from dra_utils.dbusutil import dbus_has_owner
from dra_utils.i18n import _
from dra_utils import network
from dra_client.service.client_dbus import is_client_dbus_running
from dra_server.server_dbus import is_server_dbus_running


DBUS_NAME = 'com.deepin.daemon.Remoting.Manager'
DBUS_PATH = '/com/deepin/daemon/Remoting/Manager'
DBUS_ROOT_IFACE = 'com.deepin.daemon.Remoting.Manager'

is_manager_dbus_running = lambda: dbus_has_owner(DBUS_NAME)

class ManagerDBus(dbus.service.Object):
    '''Manager dbus interface'''

    def __init__(self):
        loop = DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SessionBus(loop)
        bus_name = dbus.service.BusName(DBUS_NAME, bus=session_bus)
        server_path = dbus.service.ObjectPath(DBUS_PATH)
        super().__init__(bus_name=bus_name, object_path=server_path)
        self.properties = {
                DBUS_ROOT_IFACE: self._get_root_iface_properties(),
        }

    def _get_root_iface_properties(self):
        return {
            'Status': (self._get_status, None),
        }

    # interface properties
    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ss',
                         out_signature='v')
    def Get(self, interface, prop):
        (getter, _) = self.properties[interface][prop]
        if callable(getter):
            return getter()
        else:
            return getter

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface=DBUS_ROOT_IFACE):
        '''Get all properties'''
        getters = {}
        for key, (getter, _) in self.properties[interface].items():
            if callable(getter):
                getters[key] = getter()
            else:
                getters[key] = getter
        return getters

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ssv',
                         out_signature='')
    def Set(self, interface, prop, value):
        _, setter = self.properties[interface][prop]
        if setter:
            setter(value)
            self.PropertiesChanged(interface,
                                   {prop: self.Get(interface, prop)}, [])

    @dbus.service.signal(dbus.PROPERTIES_IFACE, signature='sa{sv}as')
    def PropertiesChanged(self, interface, changed_properties,
                          invalidated_properties):
        pass

    @dbus.service.method(DBUS_ROOT_IFACE, in_signature='', out_signature='i')
    def CheckNetworkConnectivity(self):
        '''Get network connection status'''
        return network.is_connected()

    @dbus.service.method(DBUS_ROOT_IFACE, in_signature='', out_signature='i')
    def GetStatus(self):
        '''Get remoting service status'''
        return self._get_status()

    def _get_status(self):
        if is_client_dbus_running():
            return constants.MANAGER_STATUS_CLIENT
        elif is_server_dbus_running():
            return constants.MANAGER_STATUS_SERVER
        else:
            return constants.MANAGER_STATUS_UNINITIALIZED

    @dbus.service.method(DBUS_ROOT_IFACE, in_signature='', out_signature='')
    def Stop(self):
        '''Stop remoting manager service'''
        QtCore.QCoreApplication.instance().quit()

def main():
    if is_manager_dbus_running():
        return
    app = QtCore.QCoreApplication(sys.argv)
    app.setApplicationName(_(constants.APP_NAME))
    manager_dbus = ManagerDBus()
    app.exec()

if __name__ == '__main__':
    main()
