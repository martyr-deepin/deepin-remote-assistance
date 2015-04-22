
'''Handle messages'''

import json

from PyQt5 import QtCore

from Xlib import X

from dra_utils.log import client_log
from . import constants

# mouse button orders
button_ids = (None, 1, 2, 3, 4, 5, 6, 7)

# To mark web page is loaded or not
remoting_connected = False

# Reference to client dbus object
client_dbus = None


