
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.threads_init()

# FIXME: QtMainLoop does not work
#from dbus.mainloop.pyqt5 import DBusQtMainLoop
from dbus.mainloop.glib import DBusGMainLoop
from PyQt5.QtWidgets import qApp

from . import constants
from . import client 
from . import cmd
from dra_client.mainwindowengine import MainWindowEngine
from dra_utils.log import client_log


class ClientDBus(dbus.service.Object):

    def __init__(self):
        # Init dbus main loop
        #loop = DBusQtMainLoop(set_as_default=True)
        loop = DBusGMainLoop(set_as_default=True)

        session_bus = dbus.SessionBus(loop)
        bus_name = dbus.service.BusName(constants.DBUS_NAME, bus=session_bus)
        server_path = dbus.service.ObjectPath(constants.DBUS_CLIENT_PATH)
        super().__init__(bus_name=bus_name, object_path=server_path)

        self.properties = {
                constants.DBUS_ROOT_IFACE: self._get_root_iface_properties(),
        }

        #self.engine = MainWindowEngine()
        self.engine = None

        # To mark status of client side
        self._status = constants.CLIENT_STATUS_UNINITIALIZED

    def _get_root_iface_properties(self):
        print('get all properties')
        return {
            'Status': (self._get_status, None),
        }

    # interface properties
    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ss',
                         out_signature='v')
    def Get(self, interface, prop):
        (getter, _) = self.properties[interface][prop]
        print('DBus Get:', interface, prop)
        if callable(getter):
            return getter()
        else:
            return getter

    def _get_status(self):
        print('get status:')
        return self._status

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface=constants.DBUS_ROOT_IFACE):
        '''Get all properties'''
        # TODO: remote interface argument
        print('get all:', interface)
        getters = {}
        for key, (getter, _) in self.properties[interface].items():
            if callable(getter):
                getters[key] = getter()
            else:
                getters[key] = getter
        print('getters:', getters)
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
        client_log.debug('dbus properties changed: %s:%s:%s' %
                (interface, changed_properties, invalidated_properties))

    # root iface signals
    @dbus.service.signal(constants.DBUS_ROOT_IFACE, signature='sa{sv}as')
    def StatusChanged(self, interface, changed_properties,
                          invalidated_properties):
        client_log.debug('dbus properties changed: %s:%s:%s' %
                (interface, changed_properties, invalidated_properties))

    def change_client_status(self, status):
        '''Update client status and emit a dbus signal'''
        client_log.info('change client status: %s' % status)
        self._status = status
        self.StatusChanged(constants.DBUS_ROOT_IFACE,
                           {'Status': self._status}, [])

    # root iface methods
    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Start(self):
        '''Start client side'''
        client_log.debug('start client')

        if not self.engine:
            self.engine = MainWindowEngine()
        self.engine.show()
        self.change_client_status(constants.CLIENT_STATUS_STARTED)

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Stop(self):
        '''Stop client side'''
        client_log.debug('stop client')
        self.change_client_status(constants.CLIENT_STATUS_STOPPED)
        qApp.quit()

    @dbus.service.method(constants.DBUS_ROOT_IFACE, in_signature='s',
                         out_signature='')
    def Connect(self, remote_peer_id):
        '''Connect to remote peer'''
        # Send remote peer id to browser side
        client_log.info('call cmd.init_remoting: %s' % remote_peer_id)
        self.change_client_status(constants.CLIENT_STATUS_CONNECTING)
        cmd.init_remoting(remote_peer_id)

