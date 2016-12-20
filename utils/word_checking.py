from __future__ import unicode_literals

import re

from collections import Counter


def check_for_flag_words(message, words_dict):
    """
    words_dict:
        {
        "apple": ["apples"],
        "banana": ["bananas"],
        "pineapple": ["pineapples"]
        }
    """
    cnt = Counter()
    delims = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n\x0b\x0c\r '
    pattern = r"[{}]".format(delims)
    base_words = words_dict.keys()
    variation_words = []
    for variation_array in words_dict.values():
        for word in variation_array:
            variation_words.append(word)
    all_words = base_words + variation_words
    message_array = re.split(pattern, message.lower())
    for word in message_array:
        # remove numbers from the word
        text_word = re.sub("\d", "", word)
        # handle apostrophes including unicode, ie. apple's -> apple and apples' -> apples
        formatted_word = text_word.replace(u"\u2019s", "").replace(u"s\u2019", "s").replace("'s", "").replace("s'", "s")
        if formatted_word in all_words:
            root = find_root_word(formatted_word, words_dict)
            if root:
                cnt[root] += 1
    return dict(cnt)


def find_root_word(word, words_dict):
    for base_word, variations in words_dict.iteritems():
        if word == base_word or word in variations:
            return base_word


def find_word_category(word, master_words_dict):
    for category in master_words_dict.keys():
        if word in master_words_dict[category].keys():
            return category
