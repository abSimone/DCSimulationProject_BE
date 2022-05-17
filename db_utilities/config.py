import json

config = {}

with open(r'db_utilities/config.json') as f:
    config = json.load(f)