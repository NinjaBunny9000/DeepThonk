import asynctwitch
import yaml
import os
import sys


ignore_list = [
    "nobodyYET"
]

bot_list = [
    "streamelements"
]

# Load the config file
with open(os.path.join(sys.path[0], 'config.yaml'), "r") as f:
    cfg = yaml.load(f)


def get_twitch_config():
    bot_config = asynctwitch.CommandBot(
        user=cfg['twitch']['bot_account'],
        oauth=cfg['twitch']['oauth'],
        channel=cfg['twitch']['channel'],         
        prefix=cfg['twitch']['prefix'],
        client_id=cfg['twitch']['client-id']
    )
    return bot_config


def twitch_channel():
    return cfg['twitch']['channel']

def bot_name():
    # str(cfg['twitch']['bot_account'])
    msg = "deepthonk"
    return msg

def streamer():
    return cfg['twitch']['streamer']

def welcome_msg():
    return cfg['twitch']['welcome_msg']

def is_bot_admin():
    admin = [cfg['twitch']['streamer'], cfg['twitch']['bot_admins']]

    return admin


twitch_instance = get_twitch_config()
