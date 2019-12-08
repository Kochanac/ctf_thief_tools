import json
import re

def getInfo():
	return {
		"task_id_in_url": None,
		"url_to_files": "/{filename}",
		"http?": False
	}

def parse_task(data, **kwargs):
	try:
		data = json.loads(data)["tasks"][kwargs.get("id")]
	except IndexError:
		print("Fine.")
		return {}

	task = {
		"Title": data['title'],
		"Category": data['tags'],
		"Description": data['description'],
		"Files": list(),
		"Tags": list(),
		"Solved": data["solved"],
		"Value": data['points']
	}
	
	task['Files'] = re.findall(r"files\/[0-9a-f]+\.?[a-z]*", task["Description"])

	return task

def get_meta(base, HEADERS):
	return {}