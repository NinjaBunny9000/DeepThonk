
# bot modules
# import utils
# import integrations
# import commandsBUTNOT
# import events
# import server_interface

# from utils.logger import loggymclogger as log

from initializer import Initializer
from commands import Commanderator
from twitchio.ext import commands

init = Initializer()
bot = commands.Bot(
    irc_token=init.cfg.token,
    client_id=init.cfg.client_id,
    nick=init.cfg.bot_nick,
    prefix=init.cfg.prefix,
    initial_channels=[init.cfg.channel]
)

# generate and register all the commands from the json file
cmd = Commanderator(bot)
cmd.generateCmds()

bot.run()
