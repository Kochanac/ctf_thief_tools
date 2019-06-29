import json

def getInfo():
	return {
		"task_id_in_url": -2,
		"url_to_files": "media/{filename}",
		"http?": False
	}

def parse_task(data):
	data = json.loads(data)
	task = {
		"Title": data['name'],
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
	
	for i in data['files_details']:
		task['Files'].append(i['file_field'])

	return task