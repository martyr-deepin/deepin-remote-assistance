
# Minumum port to be bound with
PORT_MIN = 20000

# Maximum port to be bound with
PORT_MAX = 20050

# Send remote peer id to browser side.
# A new remoting connection will be connected to that peer
# when client receives this message
CLIENT_MSG_INIT = 1

# Client connected to remote screen successfully
CLIENT_MSG_CONNECTED = 3

# DBus name
DBUS_NAME = 'com.deepin.daemon.Remoting.Client'
DBUS_CLIENT_PATH = '/com/deepin/daemon/Remoting/Client'
DBUS_ROOT_IFACE = 'com.deepin.daemon.Remoting.Client'

# DBus status
# Client is uninitialized
CLIENT_STATUS_UNINITIALIZED = 0

# Client window showed up
CLIENT_STATUS_STARTED = 1

# Client window is closed
CLIENT_STATUS_STOPPED = 2

# Connecting to remote peer (server side)
CLIENT_STATUS_CONNECTING = 3

# Connectted to remote peer successfully
CLIENT_STATUS_CONNECT_OK = 4

# Failed to connect to remote peer
CLIENT_STATUS_CONNECT_FAILED = 5

# To mark cmd messages used in oxide
CMD_MSG = 'CMD'

# To mark keyboard messages used in oxide
KEYBOARD_MSG = 'KEYBOARD'
