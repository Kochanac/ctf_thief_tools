import json
import re

def getInfo():
	return {
		"task_id_in_url": None,
		"url_to_files": "/{filename}",
		"http?": False,
		"custom_ids": False
	}

def parse_task(data, **kwargs):
	try:
		data = json.loads(data)["data"][kwargs.get("id")]
	except IndexError:
		print("Fine.")
		return {}

	task = {
		"Title": data['name'],
		"Category": data['category'],
		"Description": data['description'],
		"Files": data['file_set'],
		"Tags": list(),
		"Solved": data["already_solved"],
		"Value": data['score']/5
	}
	for i in range(len(task["Files"])):
		task["Files"][i] = task["Files"][i]["content"]

	return task

def get_meta(base, HEADERS):
	return {}
