
from PyQt5 import QtDBus

from . import constants

DBUS_NAME = 'org.freedesktop.NetworkManager'
DBUS_PATH = '/org/freedesktop/NetworkManager'
DBUS_IFACE = 'org.freedesktop.NetworkManager'
# State of nm is 1L when no network is connected
IS_NOT_CONNECTED = 1

__all__ = ['is_connected']

def is_connected():
    '''Check network is connected'''
    iface = NetworkInterface()
    return iface.is_connected()

class NetworkInterface(QtDBus.QDBusAbstractInterface):
    
    def __init__(self):
        system_bus = QtDBus.QDBusConnection.systemBus()
        super().__init__(DBUS_NAME, DBUS_PATH, DBUS_IFACE, system_bus, None)

    def is_connected(self):
        reply = self.call('CheckConnectivity')

        # Failed to check
        if reply.type() != QtDBus.QDBusMessage.ReplyMessage:
            print('[network]', reply.errorName(), reply.errorMessage())
            return constants.NETWORK_UNKNOWN
        state = reply.arguments()
        if len(state) == 1 and state[0] != IS_NOT_CONNECTED:
            return constants.NETWORK_CONNECTED
        else:
            return constants.NETWORK_DISCONNECTED
