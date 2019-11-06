""" Simple call/reponse commands w/o dependancies

Commands w/o any integrations or external dependancies live here. Usually
they are pretty simple commands. This is the place you'll wanna put 1-offs
and your channel-unique stuff.
"""

from config.importer import bot, twitch_channel, data
from utils.logger import loggymclogger as log
import utils.tools
from integrations.twitch.api_wrapper import interface
import os

log.debug(f"{__name__} loaded")


############################### CUSTOM COMMANDS ###############################

""" Put your custom commands below!"""

@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
    'example command'
    log.info("test") # tests logging
    await ctx.send(f'Test passed, @{ctx.author.name}!') # tests chat


####################### CALL/RESPONSE COMMAND GENERATOR #######################

class FAQGenerator:
    'Generates commands based on key-value pairs in dict object in content.py'

    commands = list()  # listyboi

    def __init__(self, name, response):
        # add the command to the list
        FAQGenerator.commands.append(name)

        # generate the bot.command
        @bot.command(name=name)
        async def call_and_response(ctx):
            await ctx.send(response)


def generate_faq():
    'generate the commands'
    for cmd, response in data.get_faq().items():
        FAQGenerator(cmd, response)

generate_faq()

# generate the faq help command
@bot.command(name='faq', aliases=['help'])
async def faq(ctx):
    commands = utils.tools.list_commands(FAQGenerator.commands)

    for msg in commands:
        await ctx.send(msg)

class CommandGenerator:
    'Generates commands based on key-value pairs in dict object in content.py'

    commands = list()  # listyboi

    def __init__(self, name, level, response, aliases=None):
        # add the command to the list
        CommandGenerator.commands.append(name)

        # generate the bot.command
        @bot.command(name=name, aliases=aliases)
        async def generated_commands(ctx):
            # TODO: no real "follower" test (can be anyone)
            if ctx.author.subscriber == 0 and level > 0:
                return
            if ctx.author.is_mod is False and level > 1:
                return
            await ctx.send(response)

def generate_cmd():
    'generate the commands'
    for cmd in data.get_cmds():
        if 'aliases' in cmd.keys():
            CommandGenerator(cmd['name'], cmd['level'], cmd['response'], cmd['aliases'])
        else:
            CommandGenerator(cmd['name'], cmd['level'], cmd['response'])

generate_cmd()


############################# OTHER MISC COMMANDS #############################

@bot.command(name='peckrank')
async def peckrank(ctx):
    'Checks rank of current stream vs 24/7 chicken stream in S&T cat on Twitch'

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


@bot.command(name="quoth")
async def quoth(ctx):
    'the raven, nevermore. nevermore.'
    token = ctx.content.split(' ', 1)  # tokenize™
    author = token[1].lower()  # match case for msg database keys
    if author[0] == '@':  # strip the @ if tagged
        author = author[1:]
    data.quoth(author)


@bot.command(name="quote")
async def quote(ctx):
    'pulls a random quote from the database'
    rando_quote = data.get_quote()   # get the quote from the data interface-thing
    msg = f"\"{rando_quote['quote']}\" - @{rando_quote['author']}"
    await ctx.send(msg)


@bot.command(name="project")
async def project(ctx):
    '!project <describe project here>'
    token = ctx.content.split(' ', 1)  # tokenize
    try:
        new_project = token[1]
    except IndexError:
        # if there's no arguments passed, then pull project info
        with open('data/project.txt') as project_file:
            project = project_file.read()

        await ctx.send(project)
    else:
        if ctx.author.is_mod:
            with open('data/project.txt', 'w+') as project_file:
                project_file.write(new_project)
            log.debug(f"{ctx.author.name} saved a new project: {new_project}")


# TODO add passing in a permissions-level to this command
@bot.command(name="addcmd")
async def addcmd(ctx):
    'adds a call/response command to the database'
    if ctx.author.is_mod == 0:
        ctx.send('yo, stop pokin around where you dont belong!')
        return
    token = ctx.content.split(' ', 2)  # tokenize™
    data.add_cmd(token[1], token[2])


# TODO: integrate into new permissions system.
@bot.command(name="addfaq")
async def addfaq(ctx):
    'adds a FAQ to the list of FAQs'
    if ctx.author.is_mod == 0:
        ctx.send('yo, stop pokin around where you dont belong!')
        return
    token = ctx.content.split(' ', 2)  # tokenize™
    data.add_faq(cmd=token[1], info=token[2])
    msg = f"New FAQ Stored! ⇒ {os.environ['TWITCH_PREFIX']}{token[1]}"
    await ctx.send(msg)


@bot.command(name='shoutouts')
async def shoutouts(ctx):
    'toggles shoutouts on or off'
    if data.get_setting('shoutouts'):
        data.set_setting('shoutouts', False)
        await ctx.send('Shoutouts are off now.')
    else:
        data.set_setting('shoutouts', True)
        await ctx.send('Shoutouts are back on!')


# TODO actually play the bigups sfx
@bot.command(name='raider')
async def raider(ctx):
    'shouts & thanks raiders'
    token = ctx.content.split(' ', 1)
    if token[1][0] == '@':
        raider = token[1][1:]
    else:
        raider = token[1]
    msg = f"ninjab1Bigups to @{raider} for the sick raid! Check them out at https://twitch.tv/{raider}"
    await ctx.send(msg)

@bot.command(name='so')
async def so(ctx):
    'shouts out a streamer'
    token = ctx.content.split(' ', 1)
    if token[1][0] == '@':
        streamer = token[1][1:]
    else:
        streamer = token[1]
    msg = f"Check out @{streamer}, a super rad streamer and friend of the channel! https://twitch.tv/{streamer}"
    await ctx.send(msg)


@bot.command(name='shitshow')
async def shitshow(ctx):
    'toggles the shitshow on and off (for craziness - BE WARNED)'

    if utils.tools.ok_or_nah(ctx, mod=True):
        return

    if data.get_setting('shitshow') is True:  # check if shitshow mode is enabled
        data.shitshow(False)  # make sfx & tts free for everyone to use
        msg = "The shitshow is over, pham."
    else:
        data.shitshow(True) # make sfx & tts sub-only
        msg = "The shitshow is ON"

    await ctx.send(msg)


@bot.command(name="xlev")
async def xlev(ctx):
    level = random.randint(0, 70)
    msg = f"@{ctx.author.name}, you're totes a {level}x dev! Congrats! 🎉"
    await ctx.send(msg)