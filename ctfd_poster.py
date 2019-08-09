#!/usr/bin/python3


import requests as req
import sys

args = sys.argv
if not (3 <= len(args) <= 8):
	print(
f"""~~~~~ CTFd poster script ~~~~~
~~~ works only on old CTFd and not properly tested ~~~
Usage: { args[0] } url cookie [value multipler] [hidden (default: False)] [category prefix] [direcrory with tasks (default: ./)] [number of threads]
tasks directory should be in format:

tasks_dir:
	task1:
		info.json
		[ file1.zip ]
	task2:
		info.json
		[ file2.py ]

info.json should contain:
	Title
	Category
	Description
	Value
	[ Tags ]
	[ Flag ]
""")
	exit(0)


# PLEASE
if len(args) == 3:
	args.append('1')

if len(args) == 4:
	args.append('False')

if len(args) == 5:
	args.append('')

if len(args) == 6:
	args.append('./')

if len(args) == 7:
	args.append('4')


url = args[1]

if url[-1] != '/':
	url += '/'

url_to_new = url + 'admin/chal/new'
cookie = args[2]
multipler = float(args[3])
hidden = {'true':True, 'false':False }[ args[4].lower() ]
prefix = args[5]
directory = args[6] 
nofworkers = int(args[7])


example = {"Title": 'title',
			"Category": "pwn",
			"Description": 'text',
			"Files": ['lox.txt', 'flag.txt'],
			"Tags": 'easy',
			"Value": 300,
			"Hidden": True,
			'Flag': 'rrrr'}

# url_to_new = 'http://ctf/admin/chal/new'

def postChal(task):
	data = {
		'name': task['Title'],
		'category': task['Category'],
		'description': task['Description'],
		'value': task["Value"],
		'key': task["Flag"],
		'key_type[0]': 'static',
		'chaltype': 'standard',
		'nonce': NONCE,
	}

	if task['Hidden']:
		data['hidden'] = 'on'

	files = list()
	for i in task['Files']:
		if i == 'info.json':
			continue
		files.append( ('files[]', (i, open(task['Folder'] + '/' + i, 'rb'))) )

	# data['files'] = files
	post = req.post(url_to_new, data=data, headers={'Cookie': cookie}, allow_redirects=False, files=files)

	if post.ok:
		print(f"[+] Posted task { task['Title'] }, Category: { task['Category'] }, { 'Hidden' if task['Hidden'] else 'Public' }")
	else:
		print('smth bad')


# import os
from multiprocessing import Pool
from os import listdir
import json, random


tasks = listdir(directory)

#nonce
resp = req.get(url_to_new, headers={'Cookie': cookie})
import re
NONCE = re.findall('nonce = "(.*)"', resp.text)[0]
# print(NONCE)

def buildTask(folder):
	task = json.loads(open(folder+'/info.json', 'r').read())
	task['Value'] *= multipler

	if "Flag" not in task:
		task["Flag"] = str(random.randint(1, int(1e100)))

	task["Hidden"] = hidden
	task["Folder"] = folder
	task["Category"] = prefix + task["Category"]

	task['Files'] = listdir(folder)
	# print(task)
	return task

jobs = [buildTask(directory+'/'+x) for x in tasks]

workers = Pool(nofworkers)

workers.map(postChal, jobs)
