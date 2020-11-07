"""Simple script to make cached json human readable"""

import os, json

DIR = os.path.dirname(__file__)
cache_folder = os.path.join(DIR, "cache")
json_folder = os.path.join(cache_folder, "json")
print()
for entry in os.scandir(json_folder):
	print(entry)
	p = os.path.join(json_folder, entry)
	with open(p, "r+") as e:
		s = json.dumps(json.loads(e.read()), indent=4)
	with open(p, "w+") as e:
		e.write(s)