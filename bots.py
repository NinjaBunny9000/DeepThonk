import asynctwitch
import conf
import cmd
import twitch_chat
import signal
import sys
import os

def start_twitch():
    # pull in the config var for ze bot!
    print('Starting Twitchbot..')
    bot = conf.twitch_instance
    bot.start()


def main():
    start_twitch()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminal-Interrupted')
        bot = conf.twitch_instance
        bot.stop(exit=True)
        os._exit(0)   