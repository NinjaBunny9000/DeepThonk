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

twitch_bot = conf.twitch_instance

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Terminal-Interrupted')
        # twitch_chat.say_goodbye()
        twitch_bot.say('ninjabunny9000', '@NinjaBunny9000 killed me! D:')
        bot = conf.twitch_instance
        bot.stop(exit=True)
        os._exit(0)   