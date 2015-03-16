
import subprocess

from dra import util

class Chromium:

    def __init__(self, app_path='/usr/bin/chromium-browser',
                 app='http://shangwoa.org:9000/screen#server',
                 user_data_dir='/tmp/deepin_remote_assitance'):
        self.app_path = app_path
        self.app = app
        self.user_data_dir = user_data_dir
        self.popen = None

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
