
import dbus

from . import constants

DBUS_NAME = 'org.freedesktop.ScreenSaver'
OBJECT_PATH = '/org/freedesktop/ScreenSaver'
INTERFACE = 'org.freedesktop.ScreenSaver'
INHIBIT = 'Inhibit'
UNINHIBIT = 'UnInhibit'

class ScreenSaver(object):

    def __init__(self):
        self._uid = 0
        self._inhibit_proxy = None
        self._uninhibit_proxy = None
        self.appname = constants.APP_NAME
        self.pid = constants.APP_SNAME

    def check(self):
        '''Check screensaver dbus service exists'''
        if self._inhibit_proxy:
            return True
        try:
            bus = dbus.SessionBus()
            interface = bus.get_object(DBUS_NAME, OBJECT_PATH)
            self._inhibit_proxy = interface.get_dbus_method(INHIBIT,
                                                            INTERFACE)
            self._uninhibit_proxy = interface.get_dbus_method(UNINHIBIT,
                                                              INTERFACE)
            return True
        except dbus.exceptions.DBusException as e:
            print(e)
            return False

    def inhibit(self):
        '''Turn off screensaver service'''
        if not self._inhibit_proxy:
            self.check()
        if not self._inhibit_proxy:
            print('[screensaver] ScreenSaver interface not support!')
            return
        if self._uid == 0:
            self._uid = self._inhibit_proxy(self.appname, self.pid)
        else:
            print('[screensaver] call inhibit() multiple times')

    def uninhibit(self):
        '''Turn on screensaver service'''
        if not self._inhibit_proxy:
            self.check()
        if not self._inhibit_proxy:
            print('[screensaver] ScreenSaver interface not support!')
            return
        if self._uid > 0:
            self._uninhibit_proxy(self._uid)
        else:
            print('[screensaver] call inibit() first')
