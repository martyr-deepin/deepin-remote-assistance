
PREFIX = /usr
PYLIB = ${DESTDIR}${PREFIX}/lib/python3/dist-packages/
DRALIB = ${DESTDIR}${PREFIX}/lib/dra
DBUSLIB = ${DESTDIR}${PREFIX}/share/dbus-1/services/
ICONS = ${DESTDIR}${PREFIX}/share/icons/

all:
	
install:
	# Create directories
	mkdir -p ${PYLIB}
	mkdir -p ${DRALIB}
	mkdir -p ${DBUSLIB}
	mkdir -p ${ICONS}
	# Copy files
	cp -rvf dra_client ${PYLIB}
	cp -rvf dra_server ${PYLIB}
	cp -rvf dra_utils ${PYLIB}
	cp -v client.py ${DRALIB}/client
	cp -v manager.py ${DRALIB}/manager
	cp -v server.py ${DRALIB}/server
	cp -v services/* ${DBUSLIB}
	cp -rvf icons/* ${ICONS}
	# Cleanup temporary files
	find ${DESTDIR}${PREFIX} -type d -iname '__pycache__' | xargs rm -rvf
	find ${DESTDIR}${PREFIX} -type f -iname '*_test*' | xargs rm -v
	# Update file permissions
	chmod -v a+x ${DRALIB}/client
	chmod -v a+x ${DRALIB}/server
	chmod -v a+x ${DRALIB}/manager
