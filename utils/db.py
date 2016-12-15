from utils import load_json, write_json


COUNTS_FILE = "data_files/counts.json"


def update_user_counts(user, count_dict):
    """
    return a dict of a user's total word counts so far,
    pass an empty dict to clear the counts for that user
    """
    # TODO this will all change once we switch to a db
    all_users_counts = load_json(COUNTS_FILE)

    if not all_users_counts:
        all_users_counts = {}
    user_counts = all_users_counts.get(user, {})
    if not user_counts:
        all_users_counts[user] = {}

    if not count_dict:
        all_users_counts[user] = {}
    else:
        user_words = user_counts.keys()
        for word, count in count_dict.iteritems():
            if word in user_words:
                user_counts[word] += count
            else:
                user_counts[word] = count
        all_users_counts[user].update(user_counts)

    print(all_users_counts)

    write_json(all_users_counts, COUNTS_FILE)

    return all_users_counts[user]
