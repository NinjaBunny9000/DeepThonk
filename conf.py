import yaml
import os
import sys

from twitchio.ext import commands

# Load the integrations config file
with open(os.path.join(sys.path[0], 'config/integrations.yaml'), "r") as f:
    integrations = yaml.load(f, Loader=yaml.FullLoader)

twitch_bot_nick = integrations['twitch']['bot_nick']
twitch_token = integrations['twitch']['token']
twitch_client_id = integrations['twitch']['client-id']
twitch_cmd_prefix = integrations['twitch']['prefix']
twitch_channel = integrations['twitch']['channel']

bot = commands.Bot(
        irc_token=twitch_token, 
        client_id=twitch_client_id, 
        nick=twitch_bot_nick, 
        prefix=twitch_cmd_prefix,
        initial_channels=[twitch_channel]
        )
