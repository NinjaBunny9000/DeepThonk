import asynctwitch
import yaml
import os
import sys

# Load the main config file
with open(os.path.join(sys.path[0], 'config/config.yaml'), "r") as f:
    cfg = yaml.load(f)

# Load the modules config file
with open(os.path.join(sys.path[0], 'config/modules.yaml'), "r") as f:
    cfg_modules = yaml.load(f)

# Load the integrations config file
with open(os.path.join(sys.path[0], 'config/integrations.yaml'), "r") as f:
    cfg_apis = yaml.load(f)

ignore_list = cfg['twitch']['ignore_list']

bot_list = cfg['twitch']['bots']

scenes = {
    'intro' : cfg['obs']['intro'],
    'main' : cfg['obs']['main'],
    'talk' : cfg['obs']['talk'],
    'brb' : cfg['obs']['brb'],
    'outro' : cfg['obs']['outro'],
    'raid' : cfg['obs']['raid'],
    'victory' : cfg['obs']['victory']
}

custom_settings = {
    "off_cmd" : cfg['bot_ctrl']['off_cmd'],
    "welcome_msg" : cfg['custom_responses']['welcome_msg'],
    "help_cmds" : cfg['twitch']['help_cmds'],
    "raid_over" : cfg['custom_responses']['raid_over'],
    "link_msg" : cfg['custom_responses']['link_msg'],
    "raid_scene" : cfg['obs']['raid_scene'],
    "raid_timer" : cfg['obs']['raid_timer'],
    "victory_scene" : cfg['obs']['victory_scene'],
    "victory_timer" : cfg['obs']['victory_timer'],
}

streamer = cfg['twitch']['streamer']

streamelements_id = cfg['streamelements']['account_id']
streamelements_auth = f"Bearer {cfg['streamelements']['jwt_token']}"
debug = cfg['bot']['debug']

strike_timeout = [cfg['moderation']['strike_1_timeout'], cfg['moderation']['strike_2_timeout']]

modules = {
    "faq" : cfg_modules['modules']['faq'],
    "lists" : cfg_modules['modules']['lists'],
    "sfx" : cfg_modules['modules']['sfx'],
    "games" : cfg_modules['modules']['games'],
    "moderation" : cfg_modules['modules']['moderation'],
    "economy" : cfg_modules['modules']['economy'],
    "obs_ctrl" : cfg_modules['modules']['obs_ctrl']
}

lists = {
    "movienight" : cfg_modules['lists']['movienight'],
    "task" : cfg_modules['lists']['task'],
    "bands" : cfg_modules['lists']['bands'],
    "comments" : cfg_modules['lists']['comments']
}

sfx = {
    "hooks_timeout" : cfg_modules['sfx']['hooks_timeout'],
    "random_timeout" : cfg_modules['sfx']['random_timeout']
}

games = {
    "raid" : cfg_modules['games']['raid'],
    "earworm_roulette" : cfg_modules['games']['earworm_roulette'],
    "cah" : cfg_modules['games']['cah']
}

moderation = {
    "strike_system" : cfg_modules['moderation']['strike_system'],
    "strike_timeout" : cfg_modules['moderation']['strike_timeout'],
    "reward_system" : cfg_modules['moderation']['reward_system']
}

economy = {
    "streamelements_points" : cfg_modules['economy']['streamelements_points'],
    "points_gifting" : cfg_modules['economy']['points_gifting']
}


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
        "link_msg" : cfg['custom_responses']['link_msg'],
        "raid_scene" : cfg['obs']['raid_scene'],
        "raid_timer" : cfg['obs']['raid_timer'],
        "victory_scene" : cfg['obs']['victory_scene'],
        "victory_timer" : cfg['obs']['victory_timer'],
    }
    return settings


def debug_yaml():
    return cfg['bot_ctrl']['off_cmd']




def twitch_channel():
    return cfg['twitch']['channel']


def bot_name():
    return str(cfg['twitch']['bot_account'])


def welcome_msg():
    return cfg['twitch']['welcome_msg']


def is_bot_admin():
    admin = [cfg['twitch']['streamer'], cfg['twitch']['bot_admins']]

    return admin


twitch_instance = get_twitch_config()
