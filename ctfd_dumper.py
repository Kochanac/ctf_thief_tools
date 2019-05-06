#!/usr/bin/python3

import requests as req
import sys



if '-h' in sys.argv:
	print(
f"""~~ CTFd dumper srcipt ~~
firstly, copy request to task json to /tmp/request

usage: {sys.argv[0]} [chals ids (default: 1-300)] [http? (default: True)] [n of threads (default: 1)]
results will be in ./task_name direcrory:

example_task
	info.json
	file1.zip
	file2.png

""")
	exit(0)

args = sys.argv[1::]


# help me
if len(args) == 0:
	args.append('1-300')

if len(args) == 1:
	args.append("True")

if len(args) == 2:
	args.append("1")

# base = args[1] # 'https://olymp.ruc.tf/' 
# cookie = args[2] # "session=3d4ba3a7-c31e-smth-9e0d5ec" 
# chals = args[3]
http = (True if args[1].lower() != 'false' else False)
Range = map(int, args[0].split('-'))
NofWorkers = int(args[2])

from utils import parse_request
url, HEADERS = parse_request(http)
url = url.split('/')[:-1]
base = '/'.join(url[:-1])+'/'
chals = '/'.join(url[-1:])+'/'


# print(url, base, chals)

from multiprocessing import Pool
from os import makedirs
import json

def getTask(url):
	j = req.get(url, headers=HEADERS)

	if not j.ok:
		# print('Error')
		return None

	print(f"[+] Got task with id { url.split('/')[-1] }")
	# print(j.text)

	pre = json.loads(j.text)#['data'] # ?????? 
	
	data = (pre['data'] if 'data' in pre else pre)

	task = {"Title": data['name'],
			"Category": data['category'],
			"Description": data['description'],
			"Files": data['files'],
			"Tags": data['tags'],
			"Value": data['value']
	}

	print(f"[^] Title: { task['Title'] }, Category: { task['Category'] }, Value: { task['Value'] }")
	try:
		makedirs(f'{task["Title"]}')

		with open(f'./{task["Title"]}/info.json', 'w') as f:
			f.write(json.dumps(task))

		for i in task['Files']:
			# print(base+'files/'+i)
			f = req.get(base+'files/'+i, headers=HEADERS).content
			with open(f'./{ task["Title"] }/{ i.split("/")[-1] }', 'wb') as file:
				file.write(f)
	except FileExistsError as e:
		print('Task is already downloaded')


workers = Pool(NofWorkers)

urls = [base+chals+str(i) for i in range(*Range)]

workers.map(getTask, urls)
