import json

def getInfo():
	return {
		"task_id_in_url": -1,
		"url_to_files": "{filename}",
		"http?": True
	}

def parse_task(data):
	data = json.loads(data)

	if "data" in data:
		data = data["data"]

	# data["files"] = [f[:f.find("?")] for f in data["files"]]

	return {
		"Title": data['name'],
		"Category": data['category'],
		"Description": data['description'],
		"Files": data['files'],
		"Tags": data['tags'],
		"Value": data['value']
	}