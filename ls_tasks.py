#!/usr/bin/env python3

import sys, json, os
from termcolor import colored as clr
from utils import *

form = "{name} - {category} {value} {solved} {files}"

if '-h' in sys.argv or '--help' in sys.argv:
	print(f"""Usage: { sys.argv[0] } [ tag ]""")
	exit(0)

args = sys.argv[1::]
if len(args) == 0:
	args.append('')

tag = args[0]

tasks = os.listdir()
for i in sorted(tasks):
	try:
		if not os.path.isdir(f'./{i}'):
			continue
		if 'info.json' not in os.listdir(f'./{i}'):
			continue

		task = json.load(open(f'./{i}/info.json'))

		if tag in task['Category']:
			print(form.format(  name = process_title(task, True)
			                  , category = process_category(task)
			                  , value = process_value(task['Value']) 
			                  , solved = process_solved(task)
			                  , files = red("[ FILES ]") if len(os.listdir(f'./{i}')) != len(task["Files"])+1 else ''
			                  )
			)

	except PermissionError:
		pass
