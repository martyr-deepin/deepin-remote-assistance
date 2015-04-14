

# Report local peer id to host service.
# This message is sent to host at a specific interval(default is 3000ms)
SERVER_MSG_ECHO = 1

# DBus name
DBUS_NAME = 'com.deepin.daemon.Remoting.Server'
DBUS_SERVER_PATH = '/com/deepin/daemon/Remoting/Server'
DBUS_ROOT_IFACE = 'com.deepin.daemon.Remoting.Server'

# DBus status
# Server is uninitialized
SERVER_STATUS_UNINITIALIZED = 0

# Server is started
SERVER_STATUS_STARTED = 1

# Server recieved new peer id
SERVER_STATUS_PEERID_OK = 2

# Server failed to get peer id
# Caused by local network connection problem
# This status is set 15s after server has been started and no valid peer id
# received
SERVER_STATUS_PEERID_FAILED = 3

# Server is connected, screen is being shared
SERVER_STATUS_SHARING = 4

# Server is stopped
SERVER_STATUS_STOPPED = 5
