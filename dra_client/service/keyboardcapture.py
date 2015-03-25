
'''
Capture global keyboard event when needed.

Note:
* CaptureController controlls CaptureWorker
* CaptureWorker is running in a QThread
* CaptureWorker contains a Capture object
* The Capture object is used to capture global keyboard event
'''

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from pykeyboard import PyKeyboardEvent

from . import keyboard


class Capture(PyKeyboardEvent, QtCore.QObject):

    tapped =QtCore.pyqtSignal(str)

    def __init__(self):
        #super().__init__()
        PyKeyboardEvent.__init__(self)
        QtCore.QObject.__init__(self)
        self.capture = True

    def escape(self, event):
        '''Override escape() method in PyKeyboardEvent.

        When True is returned, keyboard listener will be stopped.
        '''
        return False

    def tap(self, keycode, character, press):
        '''Handle keyboard event here
        
        @keycode, keyboard code
        @character, keyboard char, if available
        @press, True if event is KeyPressEvent, False if is KeyReleaseEvent
        '''
        print('tap:', keycode, character, press)
        # TODO: send this message to wssd
        #self.tapped.emit('hello')
        keyboard.send_event('hello')


class CaptureWorker(QtCore.QObject):

    tapped =QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._capture = None

    def capture(self):
        if not self._capture:
            self._capture = Capture()
            self._capture.run()
            self._capture.tapped.connect(lambda msg: self.tapped.emit(msg))

    def uncapture(self):
        if self._capture:
            self._capture.stop()
            self._capture = None


class CaptureController(QtCore.QObject):

    captured = QtCore.pyqtSignal()
    uncaptured = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.captureThread = QtCore.QThread()
        self.worker = CaptureWorker()
        self.worker.moveToThread(self.captureThread)
        self.captured.connect(self.worker.capture)
        self.uncaptured.connect(self.worker.uncapture)
        QtWidgets.qApp.aboutToQuit.connect(self.stop)

        self.captureThread.start()


    def capture(self):
        print('capturecontroller.capture')
        self.captured.emit()

    def uncapture(self):
        print('capturecontroller.uncapture')
        self.worker.uncapture()
        #self.uncaptured.emit()

    def stop(self):
        '''Stop capturing and kill background thread'''
        self.uncapture()
        if self.captureThread.isRunning():
            self.captureThread.quit()
            self.captureThread.wait(1)
