import random
import aiofiles
import aiohttp
# import logging as log
import asyncio
import os
import sys
import yaml
# import conf
import discord
from discord.ext import commands


# ─── INITIALIZATION ─────────────────────────────────────────────────────────────

with open(os.path.join(sys.path[0], 'config.yaml'), "r") as f:
    cfg = yaml.load(f)

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    global server
    global channels
    global roles

    print("Connected to discord")
    print("Logged in as:")
    print("User: {0}".format(client.user.name))
    print("ID: {0}".format(client.user.id))

    # Hardcoded server ID for NinjaFam
    server = client.get_server("159879125341962240")
    channels = dict()
    roles = dict()


    await client.change_presence(game=discord.Game(name='!help !ninjafam'))
    print('--------------------------------------------------------------------------------')


# ─── FUNCTIONS ──────────────────────────────────────────────────────────────────

def is_admin(member):
    for author_role in member.roles:
        if author_role.name == "admin":
            return True
    return False

def is_subscriber(member):
    for author_role in member.roles:
        if author_role.name == "1337 Ninjas":
            return True
    return False

def is_mod(member):
    for author_role in member.roles:
        if author_role.name == "mods":
            return True
    return False

def get_channel(requested_channel):
    for channel in server.channels:
        if channel.name == requested_channel:
            return(channel)
    else:
        return False


# ─── COMMAND SETUP ──────────────────────────────────────────────────────────────

@client.event
async def on_message(message):
    # import logging as log #TODO : This shouldn't have to be here, but it's the only way it works..

    await client.process_commands(message)  

    # Prevent bunBot from responding to itself
    if message.author == client.user:
        return
    else:
        member = server.get_member_named(str(message.author))



# ─── HELP MENUS ─────────────────────────────────────────────────────────────────
   
    # Show a help/about dialog
    if (message.content.lower().startswith("!wtf") or message.content.lower().startswith("!help")) :
        # log.info("[{0}] Requested info".format(member.name))
        msg = "Fuck you, I'm a god damn robot. Which means I have to automate various roles & features on the server so you lazy bags of meat don't have to.\n" \
            "\n**Help Menus**\n" \
            "`!wtf` or `!help` - That's this menu, dummy. #2meta4me.\n" \
            "`!superwtf` - Show commands available only to mods.\n" \
            "\n**Commands**\n" \
            "`!count` - Count how many messages you have in the channel.\n" \
            "`!subcheck` - Are you a subscriber?\n" \
            "`!modcheck` - Are you a moderator?\n" \
            "`!magic` - Be careful..\n" \
            "`!wth` - I'll be on alert..\n" \
            "\n**Voice**\n" \
            "`.join` - I'll join the voice channel you're in.\n" \
            "`.leave` - I'll leave the voice channel you're in.\n" \
            "`.play [youtube-url]` - I'll play shit.\n" \
            "`.pause` - s/e.\n" \
            "`.resume` - s/e.\n" \
            "`.stop` - s/e.\n" \
            "\nIf I'm not working correctly, go fuck yourself! You aren't my boss!!\n\nNow hurry up and do what you gotta do cuz I aint got all day! (just kidding, I'll totally out-live you puny meatsacks)"
        await client.send_message(message.channel, msg)
        return

    elif message.content.lower().startswith("!superwtf"):
        if is_mod(member):
            # log.info("[{0}] Requested mod info".format(member.name))
            msg = "Oh shit, it's a mod! Everyone pretend like you aren't fucking shit up.\n\n" \
                "`!superwtf` - This meta shit right here.\n" \
                "`!say [#channel] [message]` - Make me say shit.\n" \
                "`!stfu` - I'll take a nap.\n" \
                "`!die` - I don't want to die!!..." \
                "\n\nNow hurry up and do what you gotta do cuz I aint got all day! (just kidding, I'll totally out-live you puny meatsacks)"
        else:
            # log.info("[{0}] Requested mod info, but didn't have the required permissions".format(member.name))
            msg = "{user}, you ain't a badass in the slightest. Access denied!".format(user=member.mention)
        await client.send_message(message.channel, msg)
        return



# ─── TOOLS ──────────────────────────────────────────────────────────────────────

   

   
    # SLEEPbot9000????
    if message.content.startswith('!stfu'):
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'Done sleeping')



# ─── COMMANDS ───────────────────────────────────────────────────────────────────

    # Kills the bot (or pisses it off)
    elif message.content.lower().startswith("!die"):  # TODO : needs @mods mention working
        if is_admin(member):
            # log.info('{} killed me.'.format(message.author))
            msg = "I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, like tears in rain. Time to die."
            await client.send_message(message.channel, msg.format(user=member.mention))
            sys.exit(1)
        else:
            # log.info('{} TRIED TO KILL ME!!!'.format(message.author))
            msg = "Nice try, {user}.. But only @mods are allowed to break Rule #3. You can't kill me, you fucking scrub. "
            await client.send_message(message.channel, msg.format(user=member.mention))
        return

    # Checks if user is a subscriber
    elif message.content.lower().startswith("!subcheck"):
        if is_subscriber(member):
            passed = "Yup."
            await client.send_message(message.channel, passed)
        else:
            failed = "Nope."
            await client.send_message(message.channel, failed)
        return

    # Checks if user is a moderator
    elif message.content.lower().startswith("!modcheck"):
        if is_mod(member):
            passed = "Yup."
            await client.send_message(message.channel, passed)
        else:
            failed = "Nope."
            await client.send_message(message.channel, failed)
        return

    # Does "magic". (don't ask..)
    elif message.content.lower().startswith("!magic"):
        msg = "Congrats, {user}. You did... \"magic\"."
        await client.send_message(message.channel, msg.format(user=member.mention))
        return


    # LATENCY response



# ─── CLIENT COMMANDS ────────────────────────────────────────────────────────────


@client.command(pass_context=True)
async def _bot():
    """Is the bot cool?"""
    await client.send_message('Yes, the bot is cool.')


@client.command()
async def wth():
    await client.say('Somethin\'s fucky...')


@client.command(pass_context=True)
async def spoop(ctx, target: discord.Member = None):
    if target:
        spoopString = 0
        spoopList = os.listdir("./spoop")  # List of filenames
        spoopString = random.choice(spoopList) # Select random file from the list

        path = "./spoop/" + spoopString # Creates a string for the path to the file
        await client.say('_dials up the Spook-O-Meter.._\n\nAhh yes...🧐  ' + target.mention +'\'s rating is..')
        await client.send_file(ctx.message.channel, path)  # , filename=None, tts=False
    else:
        await client.say('You need to provide a user to rate!')


@client.command()
async def echo(*args):
    output = ""
    for word in args:
        output += word
        output += ' '
    await client.say(output)


def start_discord():
    print('Starting Discord bot...')
    client.run(cfg['discord']['token'])

start_discord()