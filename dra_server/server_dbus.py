
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.threads_init()

# FIXME: QtMainLoop does not work
#from dbus.mainloop.pyqt5 import DBusQtMainLoop
from dbus.mainloop.glib import DBusGMainLoop
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from . import constants
from . import server
from dra_utils.log import server_log


class ServerDBus(dbus.service.Object):

    def __init__(self):
        # Local Peer ID
        self._peer_id = ''

        # Connection status
        self._status = constants.SERVER_STATUS_UNINITIALIZED

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

        self.server = server.Server(self)

    def _get_root_iface_properties(self):
        return {
            'Status': (self._get_status, None),
            'PeerId': (self._get_peer_id, None),
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

    def _get_status(self):
        return self._status

    def _get_peer_id(self):
        return self._peer_id

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface=constants.DBUS_ROOT_IFACE):
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
        server_log.debug('dbus properties changed: %s:%s:%s' %
                (interface, changed_properties, invalidated_properties))

    # root iface methods
    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Start(self):
        '''Start server side'''
        server_log.debug('[dbus] start server')
        self.server.start()
        self.StatusChanged(constants.SERVER_STATUS_STARTED)

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Stop(self):
        '''Stop server side'''
        server_log.debug('[dbus] stop server')
        self.server.stop()
        self.StatusChanged(constants.SERVER_STATUS_STOPPED) 

        # Kill qApp and dbus service after 1s
        QtCore.QTimer.singleShot(1000, self.Kill)

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Kill(self):
        QtWidgets.qApp.quit()

    @dbus.service.method(constants.DBUS_ROOT_IFACE, in_signature='',
                         out_signature='s')
    def GetPeerId(self):
        return self._peer_id

    @dbus.service.method(constants.DBUS_ROOT_IFACE, in_signature='',
                         out_signature='i')
    def GetStatus(self):
        '''Get current status of server side'''
        return self._status

    @dbus.service.signal(constants.DBUS_ROOT_IFACE, signature='i')
    def StatusChanged(self, status):
        '''Server status changed'''
        server_log.info('[dbus] StatusChanged: %s' % status)
        self._status = status

        # If current status is SERVER_STATUS_PEERID_FAILED, stop service
        # TODO: call stop method in UI
        if self._status == constants.SERVER_STATUS_PEERID_FAILED:
            self.server.stop()

    def peer_id_changed(self, new_peer_id):
        '''Peer id of server side changed'''
        server_log.debug('[dbus] peer_id_changed: %s' % new_peer_id)
        # If current peer id is OK, ignore new peer id
        if self._peer_id:
            return
        # TODO: valid peer_id
        if new_peer_id:
            self.StatusChanged(constants.SERVER_STATUS_PEERID_OK)
        self._peer_id = new_peer_id
