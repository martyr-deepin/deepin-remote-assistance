
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.threads_init()

# FIXME: QtMainLoop does not work
#from dbus.mainloop.pyqt5 import DBusQtMainLoop
from dbus.mainloop.glib import DBusGMainLoop
from PyQt5.QtWidgets import qApp

from . import constants
from . import server
from dra_utils.log import server_log


class ServerDBus(dbus.service.Object):

    def __init__(self):
        self.peer_id = ''

        # Init dbus main loop
        #loop = DBusQtMainLoop(set_as_default=True)
        loop = DBusGMainLoop(set_as_default=True)

        session_bus = dbus.SessionBus(loop)
        bus_name = dbus.service.BusName(constants.DBUS_NAME, bus=session_bus)
        server_path = dbus.service.ObjectPath(constants.DBUS_SERVER_PATH)
        super().__init__(bus_name=bus_name, object_path=server_path)

        self.properties = {
                constants.DBUS_ROOT_IFACE: self._get_root_iface_properties(),
        }

        self.server = server.Server()
        self.server.peerIdUpdated.connect(self.update_peer_id)
        print('server dbus inited')

    def _get_root_iface_properties(self):
        print('get all properties')
        return {
            'Status': (self._get_status, None),
            'PeerId': (self._get_peer_id, None),
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
        return 'server status'

    def _get_peer_id(self):
        return self.peer_id

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
        server_log.debug('dbus properties changed: %s:%s:%s' %
                (interface, changed_properties, invalidated_properties))

    # root iface methods
    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Start(self):
        '''Start server side'''
        print('start server')
        server_log.debug('start server')
        self.server.start()

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Stop(self):
        '''Stop server side'''
        print('stop server')
        server_log.debug('stop server')
        self.server.stop()

        # Kill dbus service
        qApp.quit()

    def update_peer_id(self, peer_id):
        '''Update peer id'''
        print('update peer id:', peer_id)
        # TODO: check peer id existence
        self.peer_id = peer_id
        self.PropertiesChanged(constants.DBUS_ROOT_IFACE,
                               {'PeerId': peer_id}, [])
