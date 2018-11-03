import asynctwitch
import yaml
import os
import sys

# Load the config file
with open(os.path.join(sys.path[0], 'config.yaml'), "r") as f:
    cfg = yaml.load(f)
    # print(str(cfg))

def get_twitch_config():
    bot_config = asynctwitch.CommandBot(
        user=cfg['twitch']['user'],
        oauth=cfg['twitch']['oauth'],
        channel=cfg['twitch']['channel'],         
        prefix=cfg['twitch']['prefix'],
    )
    return bot_config


twitch_instance = get_twitch_config()
