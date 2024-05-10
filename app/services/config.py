import json

with open("config\\config.json") as file:
    CONFIG = json.loads(file.read())
