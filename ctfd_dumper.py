#!/usr/bin/python3

import requests as req
import sys



if not (3 <= len(sys.argv) <= 5):
	print(
f"""~~ CTFd dumper srcipt ~~
usage: {sys.argv[0]} url cookie [link to chals jsons (default: chals/)] [chals ids (default: 1-300)] [n of threads (default: 4)]
results will be in ./task_name direcrory:

example_task
	info.json
	file1.zip
	file2.png

""")
	exit(0)

args = sys.argv


# help me
if len(args) == 3:
	args.append('chals/')

if len(args) == 4:
	args.append("1-300")

if len(args) == 5:
	args.append("4")

if args[1][-1] != '/':
	args[1] += '/'

if args[3][-1] != '/':
	args[3] += '/'

if args[1][:4] != 'http':
	args[1] = f'http://{args[1]}'


base = args[1] # 'https://olymp.ruc.tf/' 
cookie = args[2] # "session=3d4ba3a7-c31e-smth-9e0d5ec" 
chals = args[3]
Range = map(int, args[4].split('-'))
NofWorkers = int(args[5])

from multiprocessing import Pool
from os import makedirs
import json

def getTask(url):
	j = req.get(url, headers={'Cookie': cookie})

	if not j.ok:
		# print('Error')
		return None

	print(f"[+] Got task with id { url.split('/')[-1] }")
	# print(j.text)

	data = json.loads(j.text)['data']
	# print(data)

	task = {"Title": data['name'],
			"Category": data['category'],
			"Description": data['description'],
			"Files": data['files'],
			"Tags": data['tags'],
			"Value": data['value']
	}

	print(f"[^] Title: { task['Title'] }, Category: { task['Category'] }, Value: { task['Value'] }")
	makedirs(f'{task["Title"]}')

	# to be removed (maybe)
	with open(f'./{task["Title"]}/info.json', 'w') as f:
		f.write(json.dumps(task))

	for i in task['Files']:
		print(base+'files/'+i)
		f = req.get(base+'files/'+i, headers={'Cookie': cookie}).content
		with open(f'./{ task["Title"] }/{ i.split("/")[-1] }', 'wb') as file:
			file.write(f)


workers = Pool(NofWorkers)

urls = [base+chals+str(i) for i in range(*Range)]

workers.map(getTask, urls)
