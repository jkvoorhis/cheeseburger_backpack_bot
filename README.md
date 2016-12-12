# cheeseburger_backpack_bot

## Clone Repo and Create Virtual Env
```
git clone git@github.com:jkvoorhis/cheeseburger_backpack_bot.git
cd cheeseburger_backpack_bot
virtualenv .
```

## Activate Virtual Env
```
. bin/activate
```

## Install dependencies
```
pip install -r requirements.txt
```

## Usage
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

## New Plugins (adding functionality)
Functionality is added through [Plugins][plugin-docs]. This project expects a certian
naming scheme in order to auto load plugins to the running bot. If you would like
your Plugin Class to be auto-loaded and used:

* Create a module in `./plugins/` named 'plugin_your_plugin_name' (snake_case)
* Name your Class within that file: 'PluginYourPluginName' (CamelCase)

Make sure your file and class names match! Files are in snake_case, and classes
are in CamelCase.

If you do not want your plugin to be automatically loaded, then do not follow this 
scheme.

## When You're Done, Deactivate Virtual Env
```
deactivate
```

[plugin-docs]: https://github.com/slackhq/python-rtmbot