import os
import sys
import yaml

from rtmbot import RtmBot

def main():
    config = yaml.load(open('rtmbot.conf', 'r'))

    debug = os.getenv('CBBP_DEBUG') #bool
    active_plugins = os.getenv('CBBP_ACTIVE_PLUGINS') #array of module paths
    slack_token = os.getenv('CBBP_SLACK_TOKEN')

    if debug is not None:
        config['DEBUG'] = debug
    if active_plugins:
        config['ACTIVE_PLUGINS'] = active_plugins
    if slack_token:
        config['SLACK_TOKEN'] = slack_token

    bot = RtmBot(config)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()