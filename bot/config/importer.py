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

# # TODO find a cleaner way to do this that doesn't involve changing var in both here and the obj def
# if all(var in os.environ for var in ("TWITCH_BOT_NICK","TWITCH_TOKEN","TWITCH_CLIENT_ID","TWITCH_PREFIX","TWITCH_CHANNEL","BOT_SERVER_KEY","STREAMLABS_KEY")):
#     continue
# else:
#     print("Hey mate, gotta give me them vars!")

from twitchio.ext import commands

# Load settings from the config obj
twitch_bot_nick = os.environ['TWITCH_BOT_NICK']
twitch_token = os.environ['TWITCH_TOKEN']
twitch_client_id = os.environ['TWITCH_CLIENT_ID']
twitch_cmd_prefix = os.environ['TWITCH_PREFIX']
twitch_channel = os.environ['TWITCH_CHANNEL']

# Instantiate a bot with teh settings & secrets
bot = commands.Bot(
        irc_token=twitch_token,
        client_id=twitch_client_id, 
        nick=twitch_bot_nick, 
        prefix=twitch_cmd_prefix,
        initial_channels=[twitch_channel]
        )

webserver_key = os.environ['BOT_SERVER_KEY']
streamlabs_key = os.environ['STREAMLABS_KEY']

sign_on_msg = "I'm back, baby!"