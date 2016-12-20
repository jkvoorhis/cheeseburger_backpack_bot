import inflect
import json

from datetime import datetime

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

def secs_till_5():
    # return the number of seconds until the next 5pm local to where run
    now = datetime.now()
    if now.hour < 17:
        next_5 = now.replace(hour=17, minute=0, second=0, microsecond=0)
    else:
        next_5 = now.replace(day=now.day + 1, hour=17, minute=0, second=0,
                               microsecond=0)
    delta_t = next_5 - now
    return delta_t.seconds + 1

