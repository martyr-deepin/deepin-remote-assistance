
from PyQt5 import QtDBus
from PyQt5 import QtCore

from . import constants
from .i18n import _

__all__ = ['notify']


class NotificationsInterface(QtDBus.QDBusAbstractInterface):
    '''Wrapup notification interface'''

    ActionInvoked = QtCore.pyqtSignal('quint32', str)
    NotificationClosed = QtCore.pyqtSignal('quint32', 'quint32')

    def __init__(self):
        session_bus = QtDBus.QDBusConnection.sessionBus()
        super().__init__(
            'org.freedesktop.Notifications',
            '/org/freedesktop/Notifications',
            'org.freedesktop.Notifications',
            session_bus,
            None)

    def notify(self, message, actions=[]):
        '''Display a notification.

        @message, string
        @actions, a list of actions
        '''
        varRPlaceId = QtCore.QVariant(0)
        varRPlaceId.convert(QtCore.QVariant.UInt)
        varActions = QtCore.QVariant(actions)
        varActions.convert(QtCore.QVariant.StringList)

        msg = self.call(
            'Notify',            # `Notify` method
            _(constants.APP_NAME),  # app name
            varRPlaceId,         # replaces_id
            constants.ICON_NAME, # app icon
            _(constants.APP_NAME),  # summary
            message,             # message body
            varActions,          # actions
            {},                  # hints
            -1                   # expire timeout, default is -1
        )
        reply = QtDBus.QDBusReply(msg)
        if reply.isValid():
            return reply.value()
        else:
            return None

def notify(*args):
    n = NotificationsInterface()
    n.notify(*args)
