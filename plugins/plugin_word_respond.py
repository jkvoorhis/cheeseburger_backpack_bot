from __future__ import unicode_literals

from rtmbot.core import Plugin

from utils import word_checking as wc_utils
from utils.utils import load_json, write_json


class PluginWordRespond(Plugin):
    def __init__(self, **kwargs):
        # because of the way plugins are called we must explicitly pass the
        # arguments to the super
        super(PluginWordRespond, self).__init__(**kwargs)
        self.words = load_json("words.json")
        self.opted_in = set(self._load_opted_in('opted_in.json'))

    def process_message(self, data):
        # TODO: for debugging only, remove for prod
        print(data)
        # trigger opt-in flow if talking directly to bot
        if data['text'].startswith("@cheeseburger_backpack"):
            self._commands(data)
            return
        # only opted-in users should experience this workflow
        if data['user'] in self.opted_in:
            word_counter = wc_utils.check_for_flag_words(
                data['text'], self.words.keys()
            )
            if word_counter:
                user_channel = self._get_user_dm_channel(data)
                mssg_kwargs = self._build_slack_count_message(
                    user_channel,
                    word_counter,
                    self.words
                )
                self.slack_client.api_call(
                    "chat.postMessage", **mssg_kwargs
                )

    def _optin_flow(self, data):
        # a bit hacky but why not reuse
        status = wc_utils.check_for_flag_words(
            data["text"],
            ["optin", "optout"]
        )
        optin = status.get("optin")
        optout = status.get("optout")

        message = {
            "channel": self._get_user_dm_channel(data),
            "as_user": "true",
            "text": "Optin Status Updated!"
        }

        if optin:
            self.opted_in.add(data["user"])
            write_json({"opted_in": list(self.opted_in)}, 'opted_in.json')
            self.slack_client.api_call("chat.postMessage", **message)

        elif optout:
            self.opted_in.discard(data["user"])
            write_json({"opted_in": list(self.opted_in)}, 'opted_in.json')
            self.slack_client.api_call("chat.postMessage", **message)

    def _build_slack_count_message(self, channel_id, count_dict, word_dict):
        result = {
            "channel": channel_id,
            "as_user": "true",
            "attachments": []
        }

        result["attachments"].append(self._build_slack_count_attachment(
            count_dict,
            word_dict
        ))

        return result

    def _build_slack_count_attachment(self, count_dict, word_dict):
        attachment_template = {
            "fallback": "Breakdown of words used, and possible "
                        "alternatives",  # fallback text
            "pretext": "Unpacking the Words You've Used:",
            "color": "#439FE0",
            "fields": [],
            "footer": "Cheeseburger Backpack",
            "mrkdwn_in": ["fields"]
        }

        for word, count in count_dict.iteritems():
            attachment_template["fields"].append({
                "title": word.capitalize(),
                "value": "Count: {count}\nAlternative(s): {alt}".format(
                    count=count,
                    alt=word_dict[word]
                ),
            })

        return attachment_template

    def _load_opted_in(self, filepath):
        # TODO this will become more complicated when we use a db
        users = load_json(filepath)
        return users["opted_in"]

    def _get_user_dm_channel(self, data):
        resp = self.slack_client.api_call('im.open', user=data['user'])
        if resp['ok']:
            return resp['channel']['id']

    def _commands(self, data):
        user_channel = self._get_user_dm_channel(data)
        opt_in_opts = ["optin", "optout"]
        user_command = data["text"]
        user_command.replace('@cheeseburger_backpack', '')
        user_command.split()
        if 'help' in user_command:
            message = {
                "channel": user_channel,
                "as_user": "true",
                "mrkdwn": "true",
                "text": "Available Commands:\n"
                        "*@cheeseburger_backpack optin* - opt yourself INTO "
                        "updates on your words usage and suggestions for "
                        "changes.\n\n"
                        "*@cheeseburger_backpack optout* - opt yourself OUT OF "
                        "updates on your words usage and suggestions for "
                        "changes.\n\n"
                        "*@cheeseburger_backpack status* - display your "
                        "optin status.\n\n"
                        "*@cheeseburger_backpack help* - display this help "
                        "message again."
            }
            self.slack_client.api_call("chat.postMessage", **message)
        elif 'status' in user_command:
            user_status = data["user"] in self.opted_in
            message = {
                "channel": user_channel,
                "as_user": "true",
                "mrkdwn": "true",
                "text": "*Optin Status:* {}".format(user_status)
            }
            self.slack_client.api_call("chat.postMessage", **message)
        # check if optin or optout is in command, but not both,
        # by comparing the two lists and returning shared values. There
        # should only be 1 value.
        elif len([i for i in opt_in_opts if i in user_command])==1:
            self._optin_flow(data)
        else:
            message = {
                "channel": user_channel,
                "as_user": "true",
                "mrkdwn": "true",
                "text": "I could not understand your request. Type:\n\n"
                        "*@cheeseburger_backpack help*\n\nto see my command "
                        "options. Note: I can only understand one command at a "
                        "time."
            }
            self.slack_client.api_call("chat.postMessage", **message)
