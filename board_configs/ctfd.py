import json

def getInfo():
	return {
		"task_id_in_url": -1,
		"url_to_files": "{filename}",
		"http?": False,
		"custom_ids": False
	}

def parse_task(data, **kwargs):
	data = json.loads(data)

	if "data" in data:
		data = data["data"]

	data["files"] = [f[:f.find("?")] for f in data["files"]]

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
	
	solved = req.get(base + "api/v1/teams/me/solves", headers=HEADERS)
	if solved.status_code != 200:
		print("Can't get metadata. You can send me url which is smth like http://host/api/v1/smth/solves or just ignore it")
		url = input("URL (or nothing): ")
		solved = req.get(base + "api/v1/teams/me/solves", headers=HEADERS)

	try:
		solved = solved.json()["data"]

		data = {}
		for i in solved:
			data[int(i["challenge_id"])] = dict()
			data[int(i["challenge_id"])]["Solved"] = True

	except Exception as e:
		print("Something went wrong with meta")
		data = {}

	return data
