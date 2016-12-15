import json
import inflect

def load_json(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        return data


def write_json(blob, filepath):
    with open(filepath, 'w') as json_file:
        json.dump(blob, json_file)

def add_plurals(data):
    p = inflect.engine()
    plural_keys = []
    plural_values = []
    for key, subdict in data.iteritems():
        plural_keys.append(p.plural(key))
        plural_values.append(data[key])
    plural_dict = dict(zip(plural_keys, plural_values))
    data.update(plural_dict)
    return data
