# cheeseburger_backpack_bot

## About the Bot
This bot helps people become aware of oppressive/appropriative 
language they use in their day to day conversations, and offers 
alternative words folks can use instead. It is intended to be an 
educational tool with the goal of assisting people who are open
and interested in changing the language they use to be kinder,
less harmful, and less alienating.

There is a provided set of default words in the `data_files`
directory. This file is a livingn document. Should you disagree
with any of its contents, or think it is missing content, please 
submit a Pull Request with changes which will be reviewed. Additionally
you, or your organization, can substitute in another list of words
to use instead of the provided one.

In order to use the bot in your Slack Team, you must:

* host it on a server according to your company's policies (suggested instructions forthcoming)
* set up the bot with a Slack [auth token for your Team][slack-bot-token]
* invite the bot into channels that the bot should track word usage in

Note: the bot will only be aware of words that are said in channels it
is a member of.

Once the bot is set up, users can opt into the service. For help
type
```
@cheeseburger_backpack help
```
in any channel the bot has membership (including a DM with the bot). 
The help message will inform users of available commands, and how to 
opt-in. Once a user is opted-in, they can continue to use Slack as 
usual. At 5pm local time, opted-in users will receive a Direct
Message containing a breakdown of words they used that day that were 
on the words list the bot tracks. It also contains suggestions
for alternative words to use, if available. This message is only visible 
to the user the counts are for.

This is still a work in progress, please be patient as changes occur
and features are added or modified.


## Developer Information

### Clone Repo and Create Virtual Env
```
git clone git@github.com:jkvoorhis/cheeseburger_backpack_bot.git
cd cheeseburger_backpack_bot
virtualenv .
```

### Activate Virtual Env
```
. bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Usage
Set your environmental overrides:

```
$ export CBBP_SLACK_TOKEN='<your-bot-token>'
$ export CBBP_DEBUG=True
```

'CBBP_SLACK_TOKEN' - your bot's api token  
'CBBP_DEBUG' - flag for Debug mode, defaults to False (aka production) if not set

To get the bot up and running, from the root of the repo run:

```
python run_cheese.py 
```

### New Plugins (adding functionality)
Functionality is added through [Plugins][plugin-docs]. This project expects a certian
naming scheme in order to auto load plugins to the running bot. If you would like
your Plugin Class to be auto-loaded and used:

* Create a module in `./plugins/` named 'plugin_your_plugin_name' (snake_case)
* Name your Class within that file: 'PluginYourPluginName' (CamelCase)

Make sure your file and class names match! Files are in snake_case, and classes
are in CamelCase.

If you do not want your plugin to be automatically loaded, then do not follow this 
scheme.

### When You're Done, Deactivate Virtual Env
```
deactivate
```

[slack-bot-token]: https://my.slack.com/services/new/bot
[plugin-docs]: https://github.com/slackhq/python-rtmbot
