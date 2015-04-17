#!/usr/bin/env python3

import json
import sys
sys.path.insert(0, '../')

from dra_server import mouse


#msg = {'localY': 145, 'type': 'mousemove', 'button': 1, 'clientY': 129, 'clientX': 624, 'localX': 665, 'offsetY': 129, 'x': 624, 'w': 1351, 'y': 129, 'offsetX': 624, 'h': 796}
#mouse.handle(None, json.dumps(msg))

msg = {'localY': 145, 'type': 'mousedown', 'button': 1, 'clientY': 129, 'clientX': 624, 'localX': 665, 'offsetY': 129, 'x': 624, 'w': 1351, 'y': 129, 'offsetX': 624, 'h': 796}

mouse.handle(None, json.dumps(msg))

msg2 = {'localY': 145, 'type': 'mouseup', 'button': 1, 'clientY': 129, 'clientX': 624, 'localX': 665, 'offsetY': 129, 'x': 624, 'w': 1351, 'y': 129, 'offsetX': 624, 'h': 796}
mouse.handle(None, json.dumps(msg2))
