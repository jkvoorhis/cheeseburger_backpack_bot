import re
from collections import Counter


def check_for_flag_words(message, words_array):
    cnt = Counter()
    delims = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n\x0b\x0c\r '
    pattern = r"[{}]".format(delims)
    message_array = re.split(pattern, message.lower())
    for word in message_array:
        formatted_word = word.replace(u"\u2019", "").replace("'", "")
        if formatted_word in words_array:
            cnt[formatted_word] += 1
    return dict(cnt)
