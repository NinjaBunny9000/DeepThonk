""" Run this to start the Twitch Bot

This is the file you run to start the bot. Loads all of the integrations below.
If you add integrations, just put them under the # bot modules section
"""

import time
import config.importer

# bot modules
import utils
# import sfx
import integrations
import commands
import events
import server_interface

from utils.logger import loggymclogger as log

try:
    import debug
except ModuleNotFoundError:
    log.info("If you want a separate script to test/debug functions, you need to rename debug-example.py to debug.py")

if __name__ == "__main__":
    config.importer.bot.run()
