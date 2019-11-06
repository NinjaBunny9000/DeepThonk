""" Debug & temporary commands in testing

 >> RENAME THIS FILE TO debug.py TO USE <<<
"""

from config.importer import bot
from utils.logger import loggymclogger as log


log.debug(f"{__name__} loaded")


@bot.command(name='ismod')
async def ismod(ctx):
    if ctx.author.is_mod:
        await ctx.send("you's a mod")
    else:
        await ctx.send("you's aint mod")
