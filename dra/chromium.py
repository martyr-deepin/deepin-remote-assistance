
import subprocess

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import qApp

from dra import util

class Chromium(QObject):

    def __init__(self, parent=None, app_path='/usr/bin/chromium-browser',
                 app='http://peer.org:9000/screen#server',
                 user_data_dir='/tmp/deepin_remote_assitance/chromium'):
        super().__init__(parent)

        self.app_path = app_path
        self.app = app
        self.user_data_dir = user_data_dir
        self.popen = None

        # Kill chromium when UI window is closed
        qApp.aboutToQuit.connect(self.stop)

    def start(self):
        self.stop()
        self.popen = util.launch_app_in_background([self.app_path,
                '--app=%s' % self.app,
                '--enable-usermedia-screen-capturing',
                '--allow-http-screen-capture',
                '--user-data-dir=%s' % self.user_data_dir,
                ])

    def stop(self):
        if self.popen:
            self.popen.terminate()
            self.popen = None
        # TODO: call popen.kill()
