import json


def load_json(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        return data


def write_json(blob, filepath):
    with open(filepath, 'w') as json_file:
        json.dump(blob, json_file)
