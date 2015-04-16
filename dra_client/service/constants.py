
# Minumum port to be bound with
PORT_MIN = 20000

# Maximum port to be bound with
PORT_MAX = 20050

# Send remote peer id to browser side.
# A new remoting connection will be connected to that peer
# when client receives this message
# Host -> Browser
CLIENT_MSG_INIT = 1

# Remote peer is unavailable
# Browser -> Host
CLIENT_MSG_UNAVAILABLE = 2

# Client connected to remote screen successfully
# Browser -> Host
CLIENT_MSG_CONNECTED = 3

# Remote peer has gone offline
# Browser -> Host
CLIENT_MSG_DISCONNECTED = 4

# Browser notifies host service that it is ready
# Browser -> Host
CLIENT_MSG_READY = 5

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

# Web page in browser is loaded and ready
# Call Connect() method in dbus only if receviing this ready signal.
# Or else oxide will be failed to setup message channel
# and remote peer id will never be sent to browser side
CLIENT_STATUS_PAGE_READY = 3

# Connecting to remote peer (server side)
CLIENT_STATUS_CONNECTING = 4

# Connectted to remote peer successfully
CLIENT_STATUS_CONNECT_OK = 5

# Failed to connect to remote peer
CLIENT_STATUS_CONNECT_FAILED = 6

CLIENT_STATUS_UNAVAILABLE = 7

# Remote peer has closed desktop sharing
CLIENT_STATUS_DISCONNECTED = 8


# To mark cmd messages used in oxide
CMD_MSG = 'CMD'

# To mark keyboard messages used in oxide
KEYBOARD_MSG = 'KEYBOARD'
