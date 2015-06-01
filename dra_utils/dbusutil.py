
import dbus

def dbus_has_owner(dbus_name):
    '''Check specic dbus service is running or not, without launching it'''
    try:
        session_bus = dbus.SessionBus()
        return session_bus.name_has_owner(dbus_name)
    except dbus.exception.DBusException as e:
        return False
