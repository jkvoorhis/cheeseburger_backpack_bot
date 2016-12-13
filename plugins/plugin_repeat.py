from __future__ import unicode_literals

import re
from collections import Counter

from rtmbot.core import Plugin


class PluginRepeat(Plugin):
    def __init__(self, slack_client=None, plugin_config=None):
        # because of the way plugins are called we must explicitly pass the
        # arguments to the super
        super(PluginRepeat, self).__init__(slack_client, plugin_config)
        self.words = self.load_word_list("words.txt")

    def process_message(self, data):
        print(data)
        if (data['channel'].startswith("C") and data['type'] == 'message'):
            word_counter = self.check_for_flag_words(data['text'])
            if word_counter:
                resp = self.slack_client.api_call('im.open', user=data['user'])
                if resp['ok']:
                    self.outputs.append([
                        resp['channel']['id'],
                        'I counted you saying the following words this many '
                        'times: \n{}'.format(word_counter)
                    ])

    def check_for_flag_words(self, message):
        cnt = Counter()
        delims = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n\x0b\x0c\r '
        pattern = r"[{}]".format(delims)
        message_array = re.split(pattern, message.lower())
        for word in message_array:
            formatted_word = word.replace(u"\u2019", "").replace("'", "")
            if formatted_word in self.words:
                cnt[formatted_word] += 1
        return dict(cnt)

    def load_word_list(self, filepath):
        with open(filepath) as f:
            words = f.read().split()
            return words
