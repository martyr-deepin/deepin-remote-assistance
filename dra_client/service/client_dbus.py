
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.threads_init()

# FIXME: QtMainLoop does not work
#from dbus.mainloop.pyqt5 import DBusQtMainLoop
from dbus.mainloop.glib import DBusGMainLoop
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from . import client 
from . import constants
from . import messaging
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

    def _get_status(self):
        return self._status

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
        client_log.debug('[dbus] properties changed: %s:%s:%s' %
                (interface, changed_properties, invalidated_properties))

    # root iface signals
    @dbus.service.signal(constants.DBUS_ROOT_IFACE, signature='i')
    def StatusChanged(self, status):
        '''Client status has been changed'''
        client_log.info('[dbus] client status changed: %s' % status)
        self._status = status

    # root iface methods
    @dbus.service.method(constants.DBUS_ROOT_IFACE, in_signature='',
                         out_signature='i')
    def GetStatus(self):
        return self._status

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Start(self):
        '''Start client side'''
        client_log.debug('[dbus] start client')

        if not self.engine:
            self.engine = MainWindowEngine(self)
        self.engine.show()
        self.StatusChanged(constants.CLIENT_STATUS_STARTED)

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Stop(self):
        '''Stop client side'''
        client_log.debug('[dbus] stop client')
        self.StatusChanged(constants.CLIENT_STATUS_STOPPED)
        self.engine.host_client.stop()

        # Kill qApp and dbus service after 1s
        QtCore.QTimer.singleShot(1000, self.kill)

    def kill(self):
        QtWidgets.qApp.quit()

    @dbus.service.method(constants.DBUS_ROOT_IFACE, in_signature='s',
                         out_signature='')
    def Connect(self, remote_peer_id):
        '''Connect to remote peer'''
        # Send remote peer id to browser side
        client_log.info('[dbus] Connect: %s' % remote_peer_id)
        self.StatusChanged(constants.CLIENT_STATUS_CONNECTING)
        messaging.init_remoting(remote_peer_id)
