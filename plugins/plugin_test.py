from __future__ import print_function
from __future__ import unicode_literals

from rtmbot.core import Plugin

class PluginTest(Plugin):

    def catch_all(self, data):
        print(data)

    def process_message(self, data):
        if data['channel'].startswith("C"):
            self.outputs.append(
                [data['channel'], 'from repeat1 "{}" in channel {}'.format(
                    data['text'], data['channel']
                )]
            )