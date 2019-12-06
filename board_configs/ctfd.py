import json

def getInfo():
	return {
		"task_id_in_url": -1,
		"url_to_files": "{filename}",
		"http?": False
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

def get_meta(base, HEADERS):
	import requests as req
	solved = req.get(base + "solves", headers=HEADERS).json()["solves"]

	data = {}
	for i in solved:
		data[str(i["chalid"])] = dict()
		data[str(i["chalid"])]["Solved"] = True

	return data
