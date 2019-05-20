#!/usr/bin/python3

import requests as req
import sys



if '-h' in sys.argv:
	print(
f"""~~ universal ctf dumper srcipt ~~
firstly, copy request to task json to /tmp/request

usage: {sys.argv[0]} board_name [range default: 1-300] [http? default: true]
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
	args.append('false')


# print(args)
board_name = args[0]
Range = list(map(int, args[1].split('-')))
Range[1] += 1 
http = (True if args[2].lower() != 'false' else False)

board = __import__(f'board_configs.{ board_name }', fromlist=('lol'))
board_info = board.getInfo()


from utils import parse_request

url, HEADERS = parse_request(http)
url = url.split('/')
# print(url)

chals = url
chals[board_info["task_id_in_url"]] = "{id}"
chals = '/'.join(chals)

base = '/'.join(url[:3]) + '/'
files = base + board_info["url_to_files"] # there should be {filename} in it

# print(url, base, chals, files)

from multiprocessing import Pool
from os import makedirs
import json
from utils import *

def getTask(url):
	j = req.get(url, headers=HEADERS)

	if not j.ok:
		print('Error')
		return None

	print(f"[+] Got task with id { url.split('/')[board_info['task_id_in_url']] }")

	# print(j.text)

	task = board.parse_task(j.text)

	print(f"[^] Title: { task['Title'] }, Category: { process_category(task) }, Value: { process_value(task['Value']) }")
	try:
		makedirs(f'{task["Title"]}')

		with open(f'./{task["Title"]}/info.json', 'w') as f:
			f.write(json.dumps(task))

		for i in task['Files']:
			f = req.get(files.format(filename=i), headers=HEADERS).content
			with open(f'./{ task["Title"] }/{ i.split("/")[-1] }', 'wb') as file:
				file.write(f)

	except FileExistsError as e:
		print('Task is already downloaded')
		print('rm -r * && !!')
		exit(0)



urls = (chals.format(id=str(i)) for i in range(*Range))

for i in urls:
	getTask(i)
