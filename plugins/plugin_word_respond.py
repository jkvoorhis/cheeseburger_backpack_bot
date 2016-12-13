from __future__ import unicode_literals
import json

from rtmbot.core import Plugin

from utils import word_checking as wc_utils


class PluginWordRespond(Plugin):
    def __init__(self, **kwargs):
        # because of the way plugins are called we must explicitly pass the
        # arguments to the super
        super(PluginWordRespond, self).__init__(**kwargs)
        self.words = self.load_word_list("words.txt")

    def process_message(self, data):
        # TODO: for debugging only, remove for prod
        print(data)
        # TODO: channel ids that start with 'C' are public channels, this is
        # temporary until we allow users to opt-in to service
        if (data['channel'].startswith("C") and data['type'] == 'message'):
            word_counter = wc_utils.check_for_flag_words(
                data['text'], self.words
            )
            if word_counter:
                resp = self.slack_client.api_call('im.open', user=data['user'])
                if resp['ok']:
                    mssg_kwargs = self._build_slack_message(
                        resp['channel']['id'],
                        word_counter
                    )
                    self.slack_client.api_call(
                        "chat.postMessage", **mssg_kwargs
                    )

    def load_word_list(self, filepath):
        with open(filepath) as f:
            words = f.read().split()
            return words

    def _build_slack_message(self, channel_id, word_dict):
        result = {
            "channel": channel_id,
            "as_user": "true",
            "attachments": []
        }

        result["attachments"].append(self._build_slack_attachment(word_dict))

        return result

    def _build_slack_attachment(self, word_dict):
        attachment_template = {
            "fallback": "Breakdown of words used, and possible "
                        "alternatives",  # fallback text
            "pretext": "Unpacking the Words You've Used:",
            "color": "#439FE0",
            "fields": [],
            "footer": "Cheeseburger Backpack",
            "mrkdwn_in": ["fields"]
        }

        for word, count in word_dict.iteritems():
            attachment_template["fields"].append({
                "title": word.capitalize(),
                "value": "Count: {count}\nAlternatives: TBD".format(count=count),
            })

        return attachment_template
