import json

def getInfo():
	return {
		"task_id_in_url": -1,
		"url_to_files": "files/{filename}"
	}

def parse_task(data):
	data = json.loads(data)
	return {
		"Title": data['name'],
		"Category": data['category'],
		"Description": data['description'],
		"Files": data['files'],
		"Tags": data['tags'],
		"Value": data['value']
	}