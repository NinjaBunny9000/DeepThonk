""" Imports settings & secrets (for integrations)

Creates objects environment variables. Also instantiates the 
Twitch bot object.

To use bot methods & commands in other scripts:
from config.importer import bot
"""

import os
import sys
import logging

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

# Feel free to customize this string!
sign_on_msg = "I'm back, baby!"