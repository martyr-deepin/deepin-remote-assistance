
'''
Capture global keyboard event when needed.

Note:
* CaptureController controlls CaptureWorker
* CaptureWorker is running in a QThread
* CaptureWorker contains a Capture object
* The Capture object is used to capture global keyboard event
'''
import json

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from pykeyboard import PyKeyboardEvent

from . import messaging


class Capture(PyKeyboardEvent):

    def __init__(self, worker):
        super().__init__()
        self.worker = worker

        #self.capture = True

#    def escape(self, event):
#        '''Override escape() method in PyKeyboardEvent.
#
#        When True is returned, keyboard listener will be stopped.
#        '''
#        return False

    def tap(self, keycode, character, press):
        '''Handle keyboard event here
        
        @keycode, keyboard code
        @character, keyboard char, if available
        @press, True if event is KeyPressEvent, False if is KeyReleaseEvent
        '''
        msg = {
            'keycode': keycode,
            'character': character,
            'press': press,
        }
        self.worker.tapped.emit(json.dumps(msg))

    def stop(self):
        print('Capture.stop()')
        PyKeyboardEvent.stop(self)


class CaptureWorker(QtCore.QObject):

    tapped = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._capture = None

    def capture(self):
        if self._capture is None:
            self._capture = Capture(self)
            self._capture.run()

    def uncapture(self):
        if self._capture:
            self._capture.stop()
            del self._capture
            self._capture = None


class CaptureController(QtCore.QObject):

    captured = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.captureThread = QtCore.QThread()
        self.worker = CaptureWorker()
        self.worker.moveToThread(self.captureThread)
        self.worker.tapped.connect(messaging.send_keyboard_event)
        self.captured.connect(self.worker.capture)
        QtWidgets.qApp.aboutToQuit.connect(self.stop)

        self.captureThread.start()

    def capture(self):
        self.captured.emit()

    def uncapture(self):
        self.worker.uncapture()

    def stop(self):
        '''Stop capturing and kill background thread'''
        self.uncapture()
        if self.captureThread.isRunning():
            self.captureThread.quit()
            self.captureThread.wait(1)
