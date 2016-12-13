from __future__ import unicode_literals

from rtmbot.core import Plugin

from utils import word_checking as wc_utils

import json

class PluginWordRespond(Plugin):
    def __init__(self, slack_client=None, plugin_config=None):
        # because of the way plugins are called we must explicitly pass the
        # arguments to the super
        super(PluginWordRespond, self).__init__(
            slack_client=slack_client,
            plugin_config=plugin_config
        )
        self.words = self.load_json("words.json")
        print(self.words)

    def process_message(self, data):
        # TODO: for debugging only, remove for prod
        print(data)
        # TODO: channel ids that start with 'C' are public channels, this is
        # temporary until we allow users to opt-in to service
        if (data['channel'].startswith("C") and data['type'] == 'message'):
            word_counter = wc_utils.check_for_flag_words(
                data['text'], self.words.keys()
            )
            if word_counter:
                resp = self.slack_client.api_call('im.open', user=data['user'])
                if resp['ok']:
                    self.outputs.append([
                        resp['channel']['id'],
                        'I counted you saying the following words this many '
                        'times: \n{}'.format(word_counter)
                    ])
                    for key, subdict in self.words.iteritems():
                        if key in word_counter:
                            suggestion = self.words[key]
                            self.outputs.append([
                                resp['channel']['id'],
                                'Try {} instead'.format(suggestion)
                            ])

    def load_word_list(self, filepath):
        with open(filepath) as f:
            words = f.read().split()
            return words

    def load_json(self, filepath):
        with open(filepath) as word_file:
            data = json.load(word_file)
            return data