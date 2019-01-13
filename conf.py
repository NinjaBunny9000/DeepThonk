import asynctwitch
import yaml
import os
import sys




bot_list = [
    "streamelements"
]


# Load the config file
with open(os.path.join(sys.path[0], 'config.yaml'), "r") as f:
    cfg = yaml.load(f)


ignore_list = cfg['twitch']['bot_admins']


def get_twitch_config():
    bot_config = asynctwitch.CommandBot(
        user=cfg['twitch']['bot_account'],
        oauth=cfg['twitch']['oauth'],
        channel=cfg['twitch']['channel'],         
        prefix=cfg['twitch']['prefix'],
        client_id=cfg['twitch']['client-id']
    )
    return bot_config


def get_custom_settings():
    settings = {
        "off_cmd" : cfg['bot_ctrl']['off_cmd'],
        "welcome_msg" : cfg['custom_responses']['welcome_msg'],
        "help_cmds" : cfg['twitch']['help_cmds'],
        "raid_over" : cfg['custom_responses']['raid_over'],
        "link_msg" : cfg['custom_responses']['link_msg']
    }
    return settings


def debug_yaml():
    return cfg['bot_ctrl']['off_cmd']

def get_obs_scenes():
    scenes = {
        'intro' : cfg['obs']['intro'],
        'main' : cfg['obs']['main'],
        'talk' : cfg['obs']['talk'],
        'brb' : cfg['obs']['brb'],
        'outro' : cfg['obs']['outro']
    }
    return scenes


def twitch_channel():
    return cfg['twitch']['channel']


def bot_name():
    return str(cfg['twitch']['bot_account'])


def streamer():
    return cfg['twitch']['streamer']


def welcome_msg():
    return cfg['twitch']['welcome_msg']


def is_bot_admin():
    admin = [cfg['twitch']['streamer'], cfg['twitch']['bot_admins']]

    return admin


twitch_instance = get_twitch_config()
