
# bot modules
# import utils
# import integrations
# import commandsBUTNOT
# import events
# import server_interface

from twitchio.ext import commands

# local modules
from initializer import Initializer
from commands import CommandManager
from logger import log

init = Initializer()
bot = commands.Bot(
    irc_token=init.cfg.token,
    client_id=init.cfg.client_id,
    nick=init.cfg.bot_nick,
    prefix=init.cfg.prefix,
    initial_channels=[init.cfg.channel]
)

# generate and register all the commands from the json file
cmd = CommandManager(bot)
cmd.importCommands('data/commands.json')
cmd.importFAQ('data/faq.json')
log.debug('Starting the bot..')
bot.run()



