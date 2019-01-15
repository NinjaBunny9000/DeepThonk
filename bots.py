import asynctwitch
import conf
import sys
import os


'Import all the bot Modules'
import twitch_events
if conf.modules['faq']:
    import faq
if conf.modules['lists']:
    import lists
if conf.modules['games']:
    import games
if conf.modules['moderation']:
    import moderation
if conf.modules['sfx']:
    key = conf.modules['sfx']
    print(f'importing sfx: {key}')
    import sfx
if conf.modules['economy']:
    import economy
if conf.debug:
    import debug

twitch_bot = conf.twitch_instance


def start_twitch():
    # pull in the config var for ze bot!
    print('Starting the Twitch bot...')
    twitch_bot.start()


def main():
    start_twitch()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted via terminal. Shutting down...')
        twitch_bot.stop(exit=True)
        os._exit(0)   