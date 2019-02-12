from integrations.twitch.irc_wrapper import CommandBot

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


# ANCHOR Master Bot Settings
###############################################################################

bot_settings = {
    "off_cmd" : cfg['bot_ctrl']['off_cmd'],
    "welcome_msg" : cfg['custom_responses']['welcome_msg'],
    "help_cmds" : cfg['bot']['help_cmds'],
    "link_msg" : cfg['custom_responses']['link_msg'],
}

bot_list = cfg_apis['twitch']['bots']
for bot in bot_list:
    bot = bot.lower()
ignore_list = cfg_apis['twitch']['ignore_list']

debug = cfg['bot']['debug']


# ANCHOR Integrations
###############################################################################

def get_twitch_config():
    bot_config = CommandBot(
        user=cfg_apis['twitch']['bot_account'],
        oauth=cfg_apis['twitch']['oauth'],
        channel=cfg_apis['twitch']['channel'],
        prefix=cfg_apis['twitch']['prefix'],
        client_id=cfg_apis['twitch']['client-id']
    )
    return bot_config

# try:
twitch_instance = get_twitch_config()
# except:
#     print('failed')

bot_name = str(cfg_apis['twitch']['bot_account'])
streamer = cfg_apis['twitch']['streamer']
twitch_channel = cfg_apis['twitch']['channel']

streamelements_id = cfg_apis['streamelements']['account_id']
streamelements_auth = f"Bearer {cfg_apis['streamelements']['jwt_token']}"

discord_token = cfg_apis['discord']['token']
discord_server = cfg_apis['discord']['server_id']


# ANCHOR Modules
###############################################################################

modules = {
    "faq" : cfg_modules['modules']['faq'] == 'True',
    "lists" : cfg_modules['modules']['lists'],
    "sfx" : cfg_modules['modules']['sfx'] == 'True',
    "games" : cfg_modules['modules']['games'] == 'True',
    "moderation" : cfg_modules['modules']['moderation'] == 'True',
    "economy" : cfg_modules['modules']['economy'] == 'True',
    "obs" : cfg_modules['modules']['obs'] == 'True'
}

moderation = {
    'strike_system' : cfg_modules['moderation']['strike_system'],
    'strike_timeout' : cfg_modules['moderation']['strike_timeout'],
    'probation_period' : cfg_modules['moderation']['probation_period'],
    'reward_system' : cfg_modules['moderation']['reward_system']
}

scenes = {
    'intro' : cfg_modules['obs']['intro'],
    'main' : cfg_modules['obs']['main'],
    'talk' : cfg_modules['obs']['talk'],
    'brb' : cfg_modules['obs']['brb'],
    'outro' : cfg_modules['obs']['outro']
}

lists = {
    "movienight" : cfg_modules['lists']['movienight'],
    "task" : cfg_modules['lists']['task'],
    "bands" : cfg_modules['lists']['bands'],
    "comments" : cfg_modules['lists']['comments']
}

sfx = {
    "hooks" : cfg_modules['sfx']['hooks'],
    "hooks_timeout" : cfg_modules['sfx']['hooks_timeout'],
    "randoms" : cfg_modules['sfx']['randoms'],
    "randoms_timeout" : cfg_modules['sfx']['randoms_timeout']
}

games = {
    "raid" : cfg_modules['games']['raid'],
    "earworm_roulette" : cfg_modules['games']['earworm_roulette'],
    "cah" : cfg_modules['games']['cah']
}

moderation = {
    "strike_system" : cfg_modules['moderation']['strike_system'],
    "probation_period" : cfg_modules['moderation']['probation_period'],
    "strike_timeout" : cfg_modules['moderation']['strike_timeout'],
    "reward_system" : cfg_modules['moderation']['reward_system'],
    "strike_1_message" : cfg_modules['moderation']['strike_1_message'],
    "strike_2_message" : cfg_modules['moderation']['strike_2_message'],
    "strike_3_message" : cfg_modules['moderation']['strike_3_message']
}

economy = {
    "streamelements_points" : cfg_modules['economy']['streamelements_points'],
    "points_gifting" : cfg_modules['economy']['points_gifting']
}

raid = {
    "home_team_name" : cfg_modules['raid']['home_team_name'],
    "away_team_name" : cfg_modules['raid']['away_team_name'],
    "max_hp" : cfg_modules['raid']['max_hp'],
    "raid_delay" : cfg_modules['raid']['raid_delay'],
    "custom_rules_scene" : cfg_modules['raid']['custom_rules_scene'],
    "custom_raid_scene" : cfg_modules['raid']['custom_raid_scene'],
    "custom_victory_scene" : cfg_modules['raid']['custom_victory_scene'],
    "rules_scene" : cfg_modules['raid']['rules_scene'],
    "raid_scene" : cfg_modules['raid']['raid_scene'],
    "victory_scene" : cfg_modules['raid']['victory_scene'],
    "rules_timer" : cfg_modules['raid']['rules_timer'],
    "victory_timer" : cfg_modules['raid']['victory_timer'],
    "raid_over" : cfg_modules['raid']['raid_over']
}