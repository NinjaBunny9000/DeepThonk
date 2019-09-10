""" Simple call/reponse commands w/o dependancies

Commands w/o any integrations or external dependancies live here. Usually
they are pretty simple commands. This is the place you'll wanna put 1-offs
and your channel-unique stuff.
"""

from config.importer import bot
from robo_interface import sio
from utils.logger import loggymclogger as log

log.debug(f"{__name__} loaded")

@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
    'example command'
    log.info("test") # tests logging
    await ctx.send(f'Test passed, @{ctx.author.name}!') # tests chat
