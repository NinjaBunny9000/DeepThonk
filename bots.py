import asynctwitch
import conf
import cmd
import twitch_chat


def start_twitch():
    # pull in the config var for ze bot!
    bot = conf.twitch_instance
    bot.start()

start_twitch()

