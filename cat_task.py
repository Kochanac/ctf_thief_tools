#!/usr/bin/env python3

import sys, json, os
from termcolor import colored as clr
from utils import *

form = """
{title} {solved}
{category} - {value}

{text}

Files:
{files}
"""

if '-h' in sys.argv or '--help' in sys.argv:
	print(f"""Usage: { sys.argv[0] } [directory or json of task]""")
	exit(0)

if len(sys.argv) == 1:
	file = 'info.json'
elif os.path.isdir(sys.argv[1]):
	file = sys.argv[1]+'/info.json'
else:
	file = sys.argv[1]


def fmt_file(x):
	if isinstance(x, str):
		return x
	if isinstance(x, dict):
		return x["name"]
	
	return x


with open(file) as f:
	data = json.loads(f.read())


	print(form.format(title = process_title(data)
	                  , category = process_category(data)
	                  , value = process_value(data["Value"])
	                  , text = process_desc(data["Description"])
	                  , files = ('\n'.join([fmt_file(file) for file in data['Files'] ]) if 'Files' in data else 'No files')
	                  ,	solved = process_solved(data)
	                 )
	)
