#!/usr/bin/env python3

import json
import sys

if '-h' in sys.argv:
	print(
f"""usage: {sys.argv[0]} info.json
""")

"""
IFS=$"                                                                                       
"

for task in $(lstasks tag | cut -d'-' -f1); 
do task=$(echo "$task" | xargs);
echo "$task" && cd "$task";
curl 'http://tasks.kochan.me/api/v1/challenges' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0' -H 'Accept: application/json' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://tasks.kochan.me/admin/challenges/new' -H 'Content-Type: application/json' -H 'CSRF-Token: b8c51c8ea10b6e6a5f7eba85eb6534ed763e7403a2dbe00933c2fa95e5c8be9c' -H 'Origin: http://tasks.kochan.me' -H 'Connection: keep-alive' -H 'Cookie: session=sess' --data "$(~/pogroming/ctf_thief_tools/ctfd_formatter.py info.json)" && cd ..;
done

"""


task = json.load(open(sys.argv[1]))

print(json.dumps(
		{
			"category": task["Category"],
			"name": task["Title"],
			"description": task["Description"],
			"type": "standard",
			"state": "visible",
			"value": task["Value"]
		}
	))