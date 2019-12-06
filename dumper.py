#!/usr/bin/env python3

import requests as req
import sys

DEBUG = False

if '-h' in sys.argv:
	print(
f"""~~ universal ctf dumper srcipt ~~
firstly, copy request to task json to /tmp/request

usage: {sys.argv[0]} board_name [range default: 1-300] [http? default depends on board]
results will be in ./task_name direcrory:

example_task
	info.json
	file1.zip
	file2.png

""")

args = sys.argv[1::]

if len(args) < 2:
	args.append('1-300')

if len(args) < 3:
	args.append('from board')


# print(args)
board_name = args[0]

Range = list(map(int, args[1].split('-')))
Range[1] += 1 

board = __import__(f'board_configs.{ board_name }', fromlist=('lol'))
board_info = board.getInfo()

http = args[2].lower()
if http == 'from board':
	http = board_info['http?']
else:
	http = (True if args[2].lower() != 'false' else False)


from utils import parse_request

url, HEADERS = parse_request(http)
url = url.split('/')
if DEBUG: print(url)

chals = url
chals[board_info["task_id_in_url"]] = "{id}"
chals = '/'.join(chals)

base = '/'.join(url[:3]) + '/'
files = base + board_info["url_to_files"] # there should be {filename} in it

if DEBUG: print(url, base, chals, files)

from os import makedirs, path
import json
from utils import *

def getTask(url):
	global files

	j = req.get(url, headers=HEADERS)

	if not j.ok:
		print('Now at id', url.split('/')[board_info['task_id_in_url']], end="\r")
		return None

	print(f"[+] Got task with id { url.split('/')[board_info['task_id_in_url']] }")

	# print(j.text)

	task = board.parse_task(j.text)

	print(f"[^] Title: { task['Title'] }, Category: { process_category(task) }, Value: { process_value(task['Value']) }")
	
	if not path.exists(task['Title']):
		makedirs(f'{task["Title"]}')
	else:
		print('Task is already downloaded')
		print('rm -r * && !!')
		exit(0)

	with open(f'./{task["Title"]}/info.json', 'w') as f:
		f.write(json.dumps(task))

	for i in task['Files']:
		f = req.get(files.format(filename=i), headers=HEADERS)

		while f.status_code != 200:
			print('Looks like there is something wrong with files url format string')
			print('You can type it yourself, filename will be placed under {filename}')
			print(f'example filename: {i}')
			files = base + input(f"{base}")

			f = req.get(files.format(filename=i), headers=HEADERS)

		with open(f'./{ task["Title"] }/{ i.split("/")[-1] }', 'wb') as file:
			file.write(f.content)



urls = (chals.format(id=str(i)) for i in range(*Range))

for i in urls:
	getTask(i)
