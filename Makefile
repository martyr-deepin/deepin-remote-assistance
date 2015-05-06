
PREFIX = /usr
PYLIB = ${DESTDIR}${PREFIX}/lib/python3/dist-packages/
DRALIB = ${DESTDIR}${PREFIX}/lib/dra
DBUSLIB = ${DESTDIR}${PREFIX}/share/dbus-1/services/

all:
	
install:
	# Make directories
	mkdir -p ${PYLIB}
	mkdir -p ${DRALIB}
	mkdir -p ${DBUSLIB}
	# Copy files
	cp -rvf dra_client ${PYLIB}
	cp -rvf dra_server ${PYLIB}
	cp -rvf dra_utils ${PYLIB}
	cp -v client.py ${DRALIB}/client
	cp -v server.py ${DRALIB}/server
	cp -v services/* ${DBUSLIB}
	# Cleanup temporary files
	find ${DESTDIR}${PREFIX} -type d -iname '__pycache__' | xargs rm -rvf
	find ${DESTDIR}${PREFIX} -type f -iname '*_test*' | xargs rm -v

