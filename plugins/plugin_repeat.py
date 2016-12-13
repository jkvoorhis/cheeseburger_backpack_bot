from __future__ import unicode_literals

import re
from collections import Counter

from rtmbot.core import Plugin

class PluginRepeat(Plugin):
    def __init__(self,slack_client=None, plugin_config=None):
        # because of the way plugins are called we must explicitly pass the
        # arguments to the super
        super(PluginRepeat, self).__init__(
            slack_client=slack_client,
            plugin_config=plugin_config
        )
        with open("words.txt") as f:
            self.words = f.read().split()

    def process_message(self, data):
        print(data)
        if (data['channel'].startswith("C") and data['type']=='message'):
            word_counter = self.check_for_flag_words(data['text'])
            if word_counter:
                resp = self.slack_client.api_call('im.open', user =data['user'])
                if resp['ok']:
                    self.outputs.append([
                        resp['channel']['id'],
                        'I counted you saying the following words this many '
                        'times: \n{}'.format(word_counter)
                    ])

    def check_for_flag_words(self, message):
        # type: (str) -> Dict
        """

        :rtype: Dict
        """
        cnt = Counter()
        delims = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n\x0b\x0c\r '
        pattern = r"[{}]".format(delims)
        message_array = re.split(pattern, message.lower())
        for word in message_array:
            word_v2 = word.replace(u"\u2019", "")
            word_v3 = word_v2.replace("'", "")
            if word_v3 in self.words:
                cnt[word_v3] += 1
        return dict(cnt)