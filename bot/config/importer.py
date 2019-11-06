""" Imports settings & secrets (for integrations)

Creates objects environment variables. Also instantiates the
Twitch bot object.

To use bot methods & commands in other scripts:
from config.importer import bot
"""

import os
import sys
import logging
import json
import random

log = logging.getLogger('deepthonk')
log.debug(f"{__name__} loaded")

# Verify the .env file has been configured
if all(var in os.environ for var in (
        "TWITCH_BOT_NICK",
        "TWITCH_TOKEN",
        "TWITCH_CLIENT_ID",
        "TWITCH_PREFIX",
        "TWITCH_CHANNEL",
        "TWITCH_TEAM",
        "BOT_SERVER_KEY",
        "STREAMLABS_KEY"
        )):
    pass
else:
    print("You need to add your secrets to the .env-example file. Be sure to rename to \".env\".")

from twitchio.ext import commands

twitch_bot_nick = os.environ['TWITCH_BOT_NICK']
twitch_token = os.environ['TWITCH_TOKEN']
twitch_client_id = os.environ['TWITCH_CLIENT_ID']
twitch_cmd_prefix = os.environ['TWITCH_PREFIX']
twitch_channel = os.environ['TWITCH_CHANNEL']
twitch_team = os.environ['TWITCH_TEAM']

# Instantiate a bot with teh settings & secrets.
bot = commands.Bot(
        irc_token=twitch_token,
        client_id=twitch_client_id,
        nick=twitch_bot_nick,
        prefix=twitch_cmd_prefix,
        initial_channels=[twitch_channel]
        )

# Other secrets we needs
webserver_key = os.environ['BOT_SERVER_KEY']
streamlabs_key = os.environ['STREAMLABS_KEY']


# IMPORT ALL THE THINGS 🧹

class DataInterface:

    # a way to construct instanced of the object (birth lil babies)
    def __init__(self):
        self.last_message = dict()

    def get_setting(self, name):

        with open('config/settings.json') as json_file:
            # return the key of the valuilee in teh json f
            data = json.load(json_file)
            return data[name]

    def set_setting(self, name, value):
        with open('config/settings.json') as json_file:
            data = json.load(json_file)  # load the file into an object
            data[name] = value  # add the k,v pair to the object
        with open('config/settings.json', 'w+') as json_file:
            json.dump(data, json_file, indent=4)  # dump a load into json file

        # TODO: double-bufffer / atomic?

    def get_faq(self):
        with open('data/faq.json') as json_file:
            return json.load(json_file)

    def add_faq(self, cmd, info):
        with open('data/faq.json') as json_file:
            data = json.load(json_file)  # load the file into an object
            data[cmd] = info  # add the k,v pair to the object
        with open('data/faq.json', 'w+') as json_file:
            json.dump(data, json_file, indent=4)  # dump a load into json file

        # commands.generate_faq()

    def add_cmd(self, cmd_name, response, level=0):
        # TODO: check for duplicates
        with open('data/commands.json') as json_file:
            data = json.load(json_file)  # load the file into an object
            list_of_cmds = list()
            for cmd in data:
                list_of_cmds.append(cmd)
            new_cmd = {
                "name" : cmd_name,
                "response" : response,
                "level" : level
            }
            list_of_cmds.append(new_cmd)
        with open('data/commands.json', 'w+') as json_file:
            json.dump(list_of_cmds, json_file, indent=4)

    def get_cmds(self):
        with open('data/commands.json') as json_file:
            return json.load(json_file)

    def rem_faq(self, cmd):
        'removes object from database/json but might not remove command'
        # TODO: make it werk
        pass

    # TODO pull from environ vars for prefix
    def save_last_message(self, author, msg):
        if msg[0] == '!':  # ignore commands
            return
        if msg[0] == '@': # strip tags if tagged
            author = author[1:]
        self.last_message[author] = msg


    def quoth(self, author):
        'take in an author name and add the last thing said from them'

        try:  # check if they've even said anything yet
            incoming_quote = {
                "author" : author,
                "quote" : self.last_message[author]
            }
        except KeyError:
            log.debug(f"{author} hasn't said anything yet...")

        # pull the json data to an object
        with open('data/quotes.json') as json_file:
            data = json.load(json_file)
            quotes = list()
            for quote in data:
                quotes.append(quote) # add all the quotes from json to a list
            quotes.append(incoming_quote) # add the new quote to the end of the list
            log.debug(f"QUOTE SAVED! {incoming_quote}")

        # rewrite with the new quote
        with open('data/quotes.json', 'w+') as json_file:
            json.dump(quotes, json_file, indent=4)  # dump it back in to json


    # TODO check for duplicates
    # TODO index quotes so we can delete/manager later
    def add_quote(self, quote, name=None):

        # dictify the quote
        quothed = {
            "author" : name,
            "quote" : quote,
        }

        # pull the json data to an object
        with open('data/quotes.json') as json_file:
            data = json.load(json_file)  # load the file into an object
            quotes = list()
            for quote in data:
                quotes.append(quote) # add all the quotes from json to a list
            quotes.append(quothed) # add the new quote to the end of the list

        # rewrite with the new quote
        with open('data/quotes.json', 'w+') as json_file:
            json.dump(quotes, json_file, indent=4)  # dump a load into json file


    def get_quote(self):
        'returns a random quote by index'
        with open('data/quotes.json') as json_file:
            data = json.load(json_file)  # load the file into an object
            quotes = list()
            for quote in data:
                quotes.append(quote) # add all the quotes from json to a list
        return random.choice(quotes)

    # TODO: literally this entire function
    def rem_quote(self, quote_num):
        pass

    def shitshow(self, mode):
        self.set_setting('shitshow', mode)
        mode = not mode
        self.set_setting('sub_only', mode)

data = DataInterface()
