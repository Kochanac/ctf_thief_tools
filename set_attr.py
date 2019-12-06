#!/usr/bin/env python3

import sys, json, os
from utils import *

if '-h' in sys.argv or '--help' in sys.argv:
	print(f"""Usage: { sys.argv[0] } attr value [directory or json of task]""")
	exit(0)

if len(sys.argv) == 3:
	file = 'info.json'
elif os.path.isdir(sys.argv[3]):
	file = sys.argv[3]+'/info.json'
else:
	file = sys.argv[3]


data = json.load(open(file, 'r'))

data[sys.argv[1]] = eval(sys.argv[2])

json.dump(data, open(file, 'w'))
