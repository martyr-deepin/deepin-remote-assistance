# About
Deepin Remote Assistance is an easy way for someone you trust, such as a friend
or technical support person, to connect to your PC and walk you through
a solution -- even if that person isn't nearby.

This project contains host service, dbus interface and desktop UI of
Deepin Remote Assistance.

# Dependencies
* [pyuserinput](https://github.com/SavinaRoja/PyUserInput), pyuserinput has a 
bug in X11 environment, see https://github.com/SavinaRoja/PyUserInput/issues/60
* [python3-tornado](https://pypi.python.org/pypi/tornado)
* dra-chromium
* python3-pyqt5
* python3-xlib
* liboxideqt-qmlplugin

# Build and Install
Run `debuild` command to generate a deb package.

# Getting involved
We encourage you to report issues and contribute changes. Please check out the [Contribution Guidelines](http://wiki.deepin.org/index.php?title=Contribution_Guidelines) about how to proceed.

# License
This project is released under GPLv3.
