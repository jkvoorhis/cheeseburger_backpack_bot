import inspect
import os
import sys
import yaml

from rtmbot import RtmBot


def main():
    config = yaml.load(open('rtmbot.conf', 'r'))

    debug = os.getenv('CBBP_DEBUG')  # bool
    active_plugins = os.getenv('CBBP_ACTIVE_PLUGINS')  # array of module paths
    slack_token = os.getenv('CBBP_SLACK_TOKEN')

    plugins = []
    for (dirpath, dirnames, filenames) in os.walk('./plugins'):
        for file in filenames:
            if file.startswith('plugin'):
                filename = file[:-3]
                class_name = ''.join(
                    x.capitalize() for x in filename.split('_')
                )
                plug = [dirpath[2:], filename, class_name]
                plugins.append('.'.join(plug))

    if debug is not None:
        config['DEBUG'] = debug
    if active_plugins:
        config['ACTIVE_PLUGINS'] = active_plugins
    else:
        config['ACTIVE_PLUGINS'] = plugins
    if slack_token:
        config['SLACK_TOKEN'] = slack_token

    bot = RtmBot(config)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
