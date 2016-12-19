import json
import inflect

def load_json(filepath):
    try:
        with open(filepath) as json_file:
            try:
                data = json.load(json_file)
                return data
            except ValueError: # file is empty
                return None
    except IOError:
        with open(filepath, 'w') as json_file:
            return None

def write_json(blob, filepath):
    with open(filepath, 'w') as json_file:
        json.dump(blob, json_file)

def add_plurals(data):
    """
    Eventually I would like this method to allow for variations of words in
    general, and not just plurals
    receive a dict of:
    {
        "apple": [],
        "banana": [],
        "pineapple": []
    }

    return:
    {
        "apple": ["apples"],
        "banana": ["bananas"],
        "pineapple": ["pineapples"]
    }
    """
    p = inflect.engine()
    for singular, plural_array in data.iteritems():
        data[singular].append(p.plural(singular))
    return data
