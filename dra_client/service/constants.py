
# Minumum port to be bound with
PORT_MIN = 20000

# Maximum port to be bound with
PORT_MAX = 20050

# Send remote peer id to browser side.
# A new remoting connection will be connected to that peer
# when client receives this message
CLIENT_MSG_INIT = 1

# DBus name
DBUS_NAME = 'com.deepin.daemon.Remoting.Client'
DBUS_CLIENT_PATH = '/com/deepin/daemon/Remoting/Client'
DBUS_ROOT_IFACE = 'com.deepin.daemon.Remoting.Client'
