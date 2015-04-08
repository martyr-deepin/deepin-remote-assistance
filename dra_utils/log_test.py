#!/usr/bin/env python3

from log import client_log
from log import server_log

def main():
    client_log.debug('client debug demo')
    server_log.info('server log demo')

if __name__ == '__main__':
    main()
