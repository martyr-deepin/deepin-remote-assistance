
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
from .views.disconnectwindow import DisconnectWindow
from dra_utils.i18n import _
from dra_utils.log import server_log
from dra_utils.notify import notify
from dra_utils.dbusutil import dbus_has_owner
from dra_utils.screensaver import ScreenSaver

is_server_dbus_running = lambda: dbus_has_owner(constants.DBUS_NAME)

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

        # Server object
        self.server = None

        # Control panel object
        self.remoting_connected = False

        # Connected to web server or not
        self.connected_to_webserver = False

        # ScreenSaver interface instance
        self.screensaver_iface = None

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
        if self.server:
            server_log.warn('[dbus] server is already running, ignore...')
            return
        server_log.debug('[dbus] start server')
        self.server = server.Server(self)
        self.server.start()
        self.StatusChanged(constants.SERVER_STATUS_STARTED)

        # Init connection-timed-out timer
        QtCore.QTimer.singleShot(constants.WEBSERVER_CONNECTION_TIMEOUT,
                                 self.on_connection_timeout)

        screensaver_iface = ScreenSaver()
        if screensaver_iface.check():
            self.screensaver_iface = screensaver_iface
            self.screensaver_iface.inhibit()

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def Stop(self):
        '''Stop server side'''
        server_log.debug('[dbus] stop server')
        if self.server:
            self.server.stop()
        self.StatusChanged(constants.SERVER_STATUS_STOPPED)

        if self.screensaver_iface:
            self.screensaver_iface.uninhibit()

        self.kill()

    @dbus.service.method(constants.DBUS_ROOT_IFACE)
    def StopNotify(self):
        '''Confirm disconnecting remoting service.

        If remoting is connected, popup confirm dialog, else, exit silently.'''
        if self.remoting_connected:
            self.disconnect_window.showConfirmWindow()
        else:
            self.Stop()

    @QtCore.pyqtSlot()
    def kill(self):
        '''Quit now'''
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

        # If failed to connect to web server, stop local service
        if self._status == constants.SERVER_STATUS_PEERID_FAILED:
            notify(_('Failed to get access code!'))
            self.Stop()

        # Get peeer ID successfully
        elif self._status == constants.SERVER_STATUS_PEERID_OK:
            self.connected_to_webserver = True

        # Show disconnection window
        elif self._status == constants.SERVER_STATUS_SHARING:
            self.remoting_connected = True
            self.disconnect_window = DisconnectWindow()
            self.disconnect_window.disconnected.connect(self.Stop)
            self.disconnect_window.show()

        # If remote peer has closed remoting connection, terminate local service
        elif self._status == constants.SERVER_STATUS_DISCONNECTED:
            notify(_('Remoting service terminated!'))
            self.Stop()

    def peer_id_changed(self, new_peer_id):
        '''Peer id of server side changed'''
        server_log.debug('[dbus] peer_id_changed: %s' % new_peer_id)
        # If current peer id is OK, ignore new peer id
        if self._peer_id:
            return
        # TODO: validate peer_id
        if new_peer_id:
            self.StatusChanged(constants.SERVER_STATUS_PEERID_OK)
        self._peer_id = new_peer_id

    @QtCore.pyqtSlot()
    def on_connection_timeout(self):
        '''Handle connection timeout signal'''
        if not self.connected_to_webserver:
            self.StatusChanged(constants.SERVER_STATUS_PEERID_FAILED)
