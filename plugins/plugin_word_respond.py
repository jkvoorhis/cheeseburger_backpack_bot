from __future__ import unicode_literals
from threading import Timer

from datetime import datetime
from rtmbot.core import Plugin

from utils import word_checking as wc_utils
from utils.db import update_user_counts, get_user_counts
from utils.utils import load_json, write_json, add_plurals

OPT_IN_FILE = "data_files/opted_in.json"
WORDS_FILE = "data_files/words.json"

class PluginWordRespond(Plugin):
    def __init__(self, **kwargs):
        # because of the way plugins are called we must explicitly pass the
        # arguments to the super
        super(PluginWordRespond, self).__init__(**kwargs)
        self.master_words = load_json(WORDS_FILE) #contains alternates
        self.words = self._make_words_list(self.master_words)
        self.categories = self.master_words.keys()
        self.opted_in = self._load_opted_in(OPT_IN_FILE)
        # timer to send private message each day at 5pm to opted in users
        x=datetime.today()
        y=x.replace(day=x.day+1, hour=17, minute=0, second=0, microsecond=0)
        delta_t=y-x
        secs=delta_t.seconds+1
        t = Timer(secs, self.job)
        t.start()

    def job(self):
        total_counts = get_user_counts()
        for user in total_counts:
            the_user = {}
            the_user["user"] = user
            user_count = total_counts.get(user)
            if not user_count:
                break;
            else:
                self._send_count_message(the_user, user_count)
                # clear the count for the user after sending the end of day message of counts
                update_user_counts(user, dict())
        # timer to send private message each day at 5pm to opted in users
        x=datetime.today()
        y=x.replace(day=x.day+1, hour=17, minute=0, second=0, microsecond=0)
        delta_t=y-x
        secs=delta_t.seconds+1
        Timer(secs, self.job).start()

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
                data['text'], self.words
            )
            if word_counter:
                total_counts = update_user_counts(data["user"], word_counter)
                print('total counts: {}'.format(total_counts))

    def _make_words_list(self, master_list):
        """
        receive:
        {
          "fruit": {
            "apple": {
              "alternatives":["asparagus"],
              "variations": ["applez"]
            },
            "banana": {
              "alternatives":["broccoli"],
              "variations": []
            },
            "pineapple": {
              "alternatives":["pea"],
              "variations": []
            }
          }
        }

        return:
        {
        "apple": ["apples", "applez"],
        "banana": ["bananas"],
        "pineapple": ["pineapples"]
        }
        """
        result = {}
        for category in master_list.values():
            for word, extras in category.iteritems():
                result[word] = extras["variations"]
        return add_plurals(result)

    def _optin_flow(self, data):
        # a bit hacky but why not reuse
        user = data['user']
        command = data["text"]
        to_check = {cat:[] for cat in self.categories}
        to_check.update({"optin":[], "optout":[]})
        status = wc_utils.check_for_flag_words(
            command,
            to_check
        )
        optin = status.get("optin")
        optout = status.get("optout")

        categories = []
        for cat in self.categories:
            if status.get(cat):
                categories.append(cat)
        message = {
            "channel": self._get_user_dm_channel(data),
            "as_user": "true",
            "text": "Optin Status Updated!"
        }

        if optin:
            set_opts = set(self.opted_in.get(user, []))
            set_opts.update(categories)
            self.opted_in[user] = list(set_opts)
        elif optout and categories:
            if self.opted_in.get(user):
                set_opts = set(self.opted_in.get(user, []))
                set_opts.difference_update(categories)
                self.opted_in[user] = list(set_opts)
        else:
            if self.opted_in.get(user):
                del self.opted_in[user]

        write_json(self.opted_in, OPT_IN_FILE)
        self.slack_client.api_call("chat.postMessage", **message)

    def _build_slack_count_message(self, channel_id, count_dict):
        result = {
            "channel": channel_id,
            "as_user": "true",
            "attachments": []
        }

        result["attachments"].append(self._build_slack_count_attachment(
            count_dict
        ))

        return result

    def _build_slack_count_attachment(self, count_dict):
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
            alt = "No alternatives."
            for category, base_word_dict in self.master_words.iteritems():
                for base_word, extra_words in base_word_dict.iteritems():
                    if word == base_word:
                        if extra_words['alternatives']:
                            alt = ', '.join(extra_words['alternatives'])
            attachment_template["fields"].append({
                "title": word.capitalize(),
                "value": "Count: {count}\nAlternative(s): {alt}".format(
                    count=count,
                    alt=alt
                ),
            })

        return attachment_template

    def _load_opted_in(self, filepath):
        # TODO this will become more complicated when we use a db
        users = load_json(filepath)
        if users:
            return users
        else:
            return {}

    def _get_user_dm_channel(self, data):
        resp = self.slack_client.api_call('im.open', user=data['user'])
        if resp['ok']:
            return resp['channel']['id']

    def _send_count_message(self, data, word_counter):
        user_channel = self._get_user_dm_channel(data)
        mssg_kwargs = self._build_slack_count_message(
            user_channel,
            word_counter
        )
        self.slack_client.api_call(
            "chat.postMessage", **mssg_kwargs
        )

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
