#!/usr/bin/python3

import requests as req
import sys

if not (3 <= len(sys.argv) <= 6):
	print(
f"""~~ ctforces dumper srcipt ~~
usage: {sys.argv[0]} cookie link_to_contest(api) [chals ids (default: 1-30)] [n of threads (default: 1)]
results will be in ./task_name direcrory:

example_task
	info.json
	file1.zip
	file2.png

""")
	exit(0)

args = sys.argv[1::]

# help me

if len(args) == 2:
	args.append('1-30')

if len(args) == 3:
	args.append('1')

cookie = args[0]
contest = args[1] + ( '/' if args[1][-1] != '/'  else '')

url = args[1] + ( '/' if args[1][-1] != '/' else '' )
url = ('http://' + url) if url[:4] != 'http' else url

ids = map(int, args[2].split('-'))
threads = int(args[3])


import json
from os import makedirs

def getTask(url):
	try:
		base = '/'.join(url.split('/')[:3])+'/'

		# print(url)
		tx = req.get(url, headers={"Cookie":cookie})

		# from requests_toolbelt.utils import dump
		# print(dump.dump_all(tx).decode())
		tx = tx.text

		data = json.loads(tx)
		# print(tx)

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
		

		print(f"[^] Title: { task['Title'] }, Category: { task['Category'] }, Value: { task['Value'] }")
		makedirs(f'{task["Title"]}')

		for i in data['files_details']:
			link = base + 'media/' + i['file_field']
			# print(link)
			task['Files'].append(i['name'])

			f = req.get(link, headers={'Cookie': cookie}).content
			with open(f'./{ task["Title"] }/{ i["name"] }', 'wb') as file:
				file.write(f)


		with open(f'./{task["Title"]}/info.json', 'w') as f:
			f.write(json.dumps(task))

	except Exception as e:
		# print(e)
		pass
		# print('No such task(')


# csrf = 'X-CSRFToken: q7kopZ1YzUnvDR1tckI3ktnJ2yeRzv1ziepcOJYkLASBWhrOKePestuFVVkTxZPl'.split(' ')[1]
# print(getTask('https://www.ctforces.com/api/contests/4/tasks/1/'))

from multiprocessing import Pool

workers = Pool(threads)

print(url)
urls = [url+f'tasks/{i}/' for i in range(*ids)]

workers.map(getTask, urls)
