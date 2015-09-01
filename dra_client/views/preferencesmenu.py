#!/usr/bin/env python3

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from dra_utils.i18n import _

# Customize styles of QMenu
MENU_STYLE = '''
QMenu {
    background-color: #151515;
    font-size: 12px;
    padding: 0px;
}

QMenu::item {
    background-color: #151515;
    color: #b4b4b4;
}

QMenu::item:hover {
    background-color: #252525;
}

QMenu::item:selected {
    background-color: #353535;
}

QMenu::separator {
    background-color: rgba(255, 255, 255, 0.1);
    height: 1px;
    margin-top: 2px;
}
'''

class PreferencesMenu(QtWidgets.QMenu):
    '''Repalce Menu class in QML.

    A serious bug exists in QML 2.2 and Deepin 2014.3, which results in
    blank screen when a qml menu popups.
    '''

    balancedChecked = QtCore.pyqtSignal()
    speedChecked = QtCore.pyqtSignal()
    qualityChecked = QtCore.pyqtSignal()
    fullscreenToggled = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        group = QtWidgets.QActionGroup(self)

        balancedAction = QtWidgets.QAction(_('Balance'), self)
        balancedAction.setCheckable(True)
        balancedAction.setChecked(True)
        balancedAction.triggered.connect(self.balancedChecked)
        balancedAction.setActionGroup(group)

        speedAction = QtWidgets.QAction(_('Optimize Speed'), self)
        speedAction.setCheckable(True)
        speedAction.triggered.connect(self.speedChecked)
        speedAction.setActionGroup(group)

        qualityAction = QtWidgets.QAction(_('Optimize Quality'), self)
        qualityAction.setCheckable(True)
        qualityAction.triggered.connect(self.qualityChecked)
        qualityAction.setActionGroup(group)

        fullscreenAction = QtWidgets.QAction(_('Fullscreen'), self)
        fullscreenAction.toggled.connect(self.fullscreenToggled)
        fullscreenAction.setCheckable(True)

        self.addAction(balancedAction)
        self.addAction(speedAction)
        self.addAction(qualityAction)
        self.addSeparator()
        self.addAction(fullscreenAction)

        self.setStyleSheet(MENU_STYLE)
