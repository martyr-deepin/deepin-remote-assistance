#!/usr/bin/env python3

import sys
sys.path.append('..')
import time

from dra.chromium import Chromium

cr = Chromium()
cr.start()

time.sleep(10)
cr.stop()
