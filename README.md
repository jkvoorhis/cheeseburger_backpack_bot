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

## When You're Done, Deactivate Virtual Env
```
deactivate
```