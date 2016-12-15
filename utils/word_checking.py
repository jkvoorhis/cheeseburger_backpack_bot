from __future__ import unicode_literals

import re

from collections import Counter


def check_for_flag_words(message, words_array):
    cnt = Counter()
    delims = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n\x0b\x0c\r '
    pattern = r"[{}]".format(delims)
    message_array = re.split(pattern, message.lower())
    for word in message_array:
        # remove numbers from the word
        text_word = re.sub("\d", "", word)
        # handle apostrophes including unicode, ie. apple's -> apple and apples' -> apples
        formatted_word = text_word.replace(u"\u2019s", "").replace(u"s\u2019", "s").replace("'s", "").replace("s'", "s")
        if formatted_word in words_array:
            cnt[formatted_word] += 1
    return dict(cnt)
