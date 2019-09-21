""" Simple call/reponse commands w/o dependancies

Commands w/o any integrations or external dependancies live here. Usually
they are pretty simple commands. This is the place you'll wanna put 1-offs
and your channel-unique stuff.
"""

from config.importer import bot, twitch_team, twitch_channel
from server_interface import sio
from utils.logger import loggymclogger as log
from content import faq_info
from utils.tools import list_commands
from integrations.twitch.api_wrapper import interface

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


# OTHER COMMANDS

@bot.command(name='peckrank')
async def peckrank(ctx):
    rank = interface._get_game_rank()
    rank_stream = rank.index(twitch_channel) + 1
    rank_opponent = rank.index('ourchickenlife') + 1 # TODO this is hardcoded #_# rip

    if rank_stream < rank_opponent:
        # TODO add viewer counts to this
        msg = f"/me 📣 WINNER WINNER CHICKEN DINNER!! 🐔 We've surpassed chikiestr3m on Science & Tech! Our rank is {rank_stream} and they're at {rank_opponent}."
        await ctx.send(msg)
        msg = f"/me If only they were a 24/7 bunny stream, things would be... different... Kappa"
        await ctx.send(msg)
    else:
        msg = f"/me 📣 We're ranked below chickiestr3m. Our rank is {rank_stream} and they're at {rank_opponent}. Maybe they should stream bunnies 24/7?? Kappa"
        await ctx.send(msg)