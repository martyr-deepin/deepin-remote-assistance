
PREFIX = /usr
PYLIB = ${DESTDIR}${PREFIX}/lib/python3/dist-packages/
DRALIB = ${DESTDIR}${PREFIX}/lib/dra
DBUSLIB = ${DESTDIR}${PREFIX}/share/dbus-1/services/
ICONS = ${DESTDIR}${PREFIX}/share/icons/
LOCALE = ${DESTDIR}${PREFIX}/share/locale
BIN = ${DESTDIR}${PREFIX}/bin
APPLICATIONS = ${DESTDIR}${PREFIX}/share/applications/

all: build

build: gui-port

gui-port:
	cd gui_port ; qmake && make

install:
	# Create directories
	mkdir -p ${PYLIB}
	mkdir -p ${DRALIB}
	mkdir -p ${DBUSLIB}
	mkdir -p ${ICONS}
	mkdir -p ${BIN}
	mkdir -p ${APPLICATIONS}
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
#	find ${DESTDIR}${PREFIX} -type d -iname '__pycache__' | xargs rm -rvf
#	find ${DESTDIR}${PREFIX} -type f -iname '*_test*' | xargs rm -v
	# Update file permissions
	chmod -v a+x ${DRALIB}/client
	chmod -v a+x ${DRALIB}/server
	chmod -v a+x ${DRALIB}/manager
	# Generate mo files
	for locale in $(shell cd locale; ls *.po); do \
		mkdir -p ${LOCALE}/$${locale%.*}/LC_MESSAGES; \
		msgfmt locale/$$locale -o ${LOCALE}/$${locale%.*}/LC_MESSAGES/deepin-remote-assistance.mo; \
	done

	#install gui-port
	install -D gui_port/deepin-remote-assistance ${BIN}
	install -D gui_port/deepin-remote-assistance.desktop ${APPLICATIONS}
	mkdir -pv ${DESTDIR}${PREFIX}/share/deepin-remote-assistance/translations
	cp -rvf gui_port/translations/*  ${DESTDIR}${PREFIX}/share/deepin-remote-assistance/translations

clean:
	-cd gui_port ;make clean;rm Makefile remote_assistance
