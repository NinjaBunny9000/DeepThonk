""" Run this to start the Twitch Bot

This is the file you run to start the bot. Loads all of the integrations below.
If you add integrations, just put them under the # bot modules section
"""

import time
import config

# bot modules
import utils
# import sfx
import commands
import events
import robo_interface
import robo_commands
import debug
import integrations

if __name__ == "__main__":
    config.importer.bot.run()
