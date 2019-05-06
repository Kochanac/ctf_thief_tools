#!/usr/bin/python3

import requests as req
import sys

if '-h' in sys.argv:
	print(
f"""~~ ctforces dumper srcipt ~~
firstly, copy request to task to /tmp/request

usage: {sys.argv[0]} [chals ids (default: 1-40)] [ http? default: False ] [n of threads (default: 1)] [debug: false if isn't set]
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
	args.append('1-40')

if len(args) == 1:
	args.append('False')

if len(args) == 2:
	args.append('1')

if len(args) == 3:
	debug = False
else:
	debug = True

http = True if args[1].lower() == "true" else False

ids = map(int, args[0].split('-'))
threads = int(args[2])

# Now we need to parse request

from utils import parse_request
url, HEADERS = parse_request(http)
url = '/'.join(url.split('/')[:-3])+'/'
print(url)

import json
from os import makedirs

def getTask(url):
	try:
		base = '/'.join(url.split('/')[:3])+'/'
		if debug:
			print(url)
		tx = req.get(url, headers=HEADERS)

		# from requests_toolbelt.utils import dump
		# print(dump.dump_all(tx).decode())
		tx = tx.text
		
		if debug:
			print(tx)
		data = json.loads(tx)
		

		task = {"Title": data['name'],
				"Category": data['tags_details'][0]['name'],
				"Description": data['description'] + f"\n\n(from ctforces, author: { data['author_username'] })",
				"Files": list(),
				# "Tags": data['tags'],
				"Solved": data["is_solved_by_user"],
				"Value": data['contest_cost']
		}

		task['Tags'] = list()
		for i in data['tags_details']:
			task['Tags'].append(i['name'])
		

		print(f"[+] Title: { task['Title'] }, Category: { task['Category'] }, Value: { task['Value'] }")
		makedirs(f'{task["Title"]}')

		for i in data['files_details']:
			link = base + 'media/' + i['file_field']
			# print(link)
			task['Files'].append(i['name'])

			f = req.get(link, headers=HEADERS).content
			with open(f'./{ task["Title"] }/{ i["name"] }', 'wb') as file:
				file.write(f)


		with open(f'./{task["Title"]}/info.json', 'w') as f:
			f.write(json.dumps(task))

	except Exception as e:
		if 'detail' in data and data['detail'] == 'No such task.':
			print(url + ' no such task')

		if debug:
			raise e

		pass


# csrf = 'X-CSRFToken: q7kopZ1YzUnvDR1tckI3ktnJ2yeRzv1ziepcOJYkLASBWhrOKePestuFVVkTxZPl'.split(' ')[1]
# print(getTask('https://www.ctforces.com/api/contests/4/tasks/1/'))

from multiprocessing import Pool

workers = Pool(threads)

print(url)
urls = [url+f'tasks/{i}/' for i in range(*ids)]

workers.map(getTask, urls)
