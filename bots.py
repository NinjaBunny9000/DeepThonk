import asynctwitch
import conf
import cmd
import twitch_chat
import signal
import sys
import os

"""
DEBUG/DEV/WIP NOTES:

Currently the Discord module is *not* being called right now. You can still run it separately
by just doing "python discord_chat.py" or whatever. WIP <3
"""

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