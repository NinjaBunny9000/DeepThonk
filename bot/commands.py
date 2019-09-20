""" Simple call/reponse commands w/o dependancies

Commands w/o any integrations or external dependancies live here. Usually
they are pretty simple commands. This is the place you'll wanna put 1-offs
and your channel-unique stuff.
"""

from config.importer import bot
from server_interface import sio
from utils.logger import loggymclogger as log
from content import faq_info
from utils.tools import list_commands

log.debug(f"{__name__} loaded")

@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
    'example command'
    log.info("test") # tests logging
    await ctx.send(f'Test passed, @{ctx.author.name}!') # tests chat



class CommandGenerator:

    # listyboi
    commands = list()

    def __init__(self, name, response):
        # add the command to the list
        CommandGenerator.commands.append(name)
        
        # generate the bot.command
        @bot.command(name=name)
        async def call_and_response(ctx):
            await ctx.send(response)

        log.debug(f"!{name} registered as a command!")

# generate the call / response commands
for cmd, response in faq_info.items():
    CommandGenerator(cmd, response)

log.info(f"Generated these commands: {CommandGenerator.commands}")

# generate the faq help command
@bot.command(name='faq', aliases=['help'])
async def faq(ctx):
    commands = list_commands(CommandGenerator.commands)

    for msg in commands:
        await ctx.send(msg)