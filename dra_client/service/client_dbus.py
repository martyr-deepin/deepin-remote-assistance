
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.threads_init()

# FIXME: QtMainLoop does not work
#from dbus.mainloop.pyqt5 import DBusQtMainLoop
from dbus.mainloop.glib import DBusGMainLoop
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from . import cmd
from .client import Client 
from . import constants
from dra_client.views.mainwindow import MainWindow
from dra_utils.dbusutil import dbus_has_owner
from dra_utils.log import client_log
from dra_utils.notify import notify

is_client_dbus_running = lambda: dbus_has_owner(constants.DBUS_NAME)

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

        # MainWindow object
        self.main_window = None

        # Client object
        self.client_host = None

        # Connected to web server or not
        self.connected_to_webserver = False

        # To mark remoting connection has been established
        self.remoting_connected = False

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

        # Connect to web server OK
        if self._status == constants.CLIENT_STATUS_PAGE_READY:
            self.connected_to_webserver = True

        # Connect to web server failed
        elif self._status == constants.CLIENT_STATUS_CONNECT_FAILED:
            self.Stop()

        # Connect to remote peer OK
        elif self._status == constants.CLIENT_STATUS_CONNECT_OK:
            self.remoting_connected = True

        # Disconnected, by remote peer or network failed
        elif self._status == constants.CLIENT_STATUS_DISCONNECTED:
            notify('Remoting service terminated!')
            self.Stop()

    # root iface methods
    @dbus.service.method(constants.DBUS_ROOT_IFACE, in_signature='',
                         out_signature='i')
    def GetStatus(self):
        return self._status

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Start(self):
        '''Start client side'''
        client_log.debug('[dbus] start client')

        if self._status >= constants.CLIENT_STATUS_STARTED:
            client_log.warn('[dbus] already started: %s' % self._status)
            return

        self.main_window = MainWindow()

        # Stop host service when main window is closed
        if not self.main_window:
            client_host.critical('[dbus] Failed to init main window!')
            self.Stop()
        self.main_window.root.windowClosed.connect(self.Stop)
        self.main_window.show()

        self.client_host = Client(self)
        self.client_host.start()

        self.StatusChanged(constants.CLIENT_STATUS_STARTED)

        # Init connection-timed-out timer
        QtCore.QTimer.singleShot(constants.WEBSERVER_CONNECTION_TIMEOUT,
                                 self.on_connection_timeout)

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Stop(self):
        '''Stop client side'''
        client_log.debug('[dbus] stop client')
        self.StatusChanged(constants.CLIENT_STATUS_STOPPED)
        if self.client_host:
            self.client_host.stop()

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
        cmd.init_remoting(remote_peer_id)

    @QtCore.pyqtSlot()
    def on_connection_timeout(self):
        '''Handle connection timeout signal'''
        if not self.connected_to_webserver:
            self.StatusChanged(constants.CLIENT_STATUS_CONNECT_FAILED)
