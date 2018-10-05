#!/usr/bin/python3.6
import argparse
import logging as log
import asyncio
import sys
import os
import random
import yaml
import textwrap
import aiofiles
import aiohttp
import time
import datetime
import youtube_dl
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient



# ─── SETUP LOGGING AND DEBUGGING ───────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Handle the various automation functions for a discord server.")
parser.add_argument("-v", "--verbose", dest="verbose", action="store_const",
                    const=True, default=False,
                    help="verbose output")
parser.add_argument("-q", "--quiet", dest="quiet", action="store_const",
                    const=True, default=False,
                    help="only output warnings and errors")
args = parser.parse_args()

if args.verbose:
    log.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=log.DEBUG, stream=sys.stdout)
    log.debug("Verbose output enabled")
elif args.quiet:
    log.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=log.WARNING, stream=sys.stdout)
else:
    log.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=log.INFO, stream=sys.stdout)

# Load the config file
with open(os.path.join(sys.path[0], 'config.yaml'), "r") as f:
    config = yaml.load(f)

# Status report
log.info("bunBot9000 is booting up...")



# ─── INITIALIZATION ─────────────────────────────────────────────────────────────

# client = discord.Client()
client = commands.Bot(command_prefix='.')

players = {}  # setup youtube player

@client.event
async def on_ready():
    global server
    global channels
    global roles
    global log

    server = client.get_server(config['discord']['server_id'])
    channels = dict()
    roles = dict()

    log.info("Connected to server: {}".format(server.name))
    log.debug("Logged in as:")
    log.debug("User: {0}".format(client.user.name))
    log.debug("ID: {0}".format(client.user.id))
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
    import logging as log #TODO : This shouldn't have to be here, but it's the only way it works..

    await client.process_commands(message)  

    #Prevent bunBot from responding to itself
    if message.author == client.user:
        return
    else :
        member = server.get_member_named(str(message.author))



# ─── HELP MENUS ─────────────────────────────────────────────────────────────────
   
    # Show a help/about dialog
    if (message.content.lower().startswith("!wtf") or message.content.lower().startswith("!help")) :
        log.info("[{0}] Requested info".format(member.name))
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
            log.info("[{0}] Requested mod info".format(member.name))
            msg = "Oh shit, it's a mod! Everyone pretend like you aren't fucking shit up.\n\n" \
                "`!superwtf` - This meta shit right here.\n" \
                "`!say [#channel] [message]` - Make me say shit.\n" \
                "`!stfu` - I'll take a nap.\n" \
                "`!die` - I don't want to die!!..." \
                "\n\nNow hurry up and do what you gotta do cuz I aint got all day! (just kidding, I'll totally out-live you puny meatsacks)"
        else:
            log.info("[{0}] Requested mod info, but didn't have the required permissions".format(member.name))
            msg = "{user}, you ain't a badass in the slightest. Access denied!".format(user=member.mention)
        await client.send_message(message.channel, msg)
        return



# ─── TOOLS ──────────────────────────────────────────────────────────────────────

    #Post a message as bunBot9000 - borrowed (very gratefully) from WaifuBot
    if message.content.lower().startswith("!say"):
        if not message.channel.is_private and is_mod(member):
            message_parts = message.content.split(' ', 2)
            if len(message.channel_mentions) == 1 and (len(message_parts) == 3 or len(message.attachments) > 0):
                channel = message.channel_mentions[0]
                if len(message.attachments) == 0:
                    msg = ""
                    if len(message_parts) == 3:
                        msg = message_parts[2]
                    await client.send_message(channel, msg)
                else:
                    for index, attachment in enumerate(message.attachments):
                        url = attachment["url"]
                        file_name = url.split('/')[-1]
                        msg = ""
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as resp:
                                data = await resp.read()
                            async with aiofiles.open(os.path.join(sys.path[0], file_name), 'wb') as file:
                                await file.write(data)
                        if index == 0:
                            if len(message_parts) == 3:
                                msg = message_parts[2]
                        await client.send_file(channel, fp=os.path.join(sys.path[0], file_name), content=msg)
                        os.remove(os.path.join(sys.path[0], file_name))
                notification_msg = "{user} made me say something in {channel}."
                await client.send_message(get_channel("test-zone"), notification_msg.format(user=member.mention, channel=channel.mention))
            else:
                msg = "Please use the following syntax: `!say [channel_mention] [message_body]`"
                await client.send_message(message.channel, msg)
        else:
            msg = "Just what do you think you're doing? You're not authorized."
            await client.send_file(message.channel, os.path.join(sys.path[0], 'dennis.gif'), filename=None, content=msg, tts=False)
        return

    # COUNT how many messages a user has sent in a given channel.
    elif message.content.startswith('!count'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    # SLEEPbot9000????
    elif message.content.startswith('!stfu'):
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'Done sleeping')



# ─── COMMANDS ───────────────────────────────────────────────────────────────────

    # Kills the bot (or pisses it off)
    elif message.content.lower().startswith("!die"):  # TODO : needs @mods mention working
        if is_admin(member):
            log.info('{} killed me.'.format(message.author))
            msg = "I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, like tears in rain. Time to die."
            await client.send_message(message.channel, msg.format(user=member.mention))
            sys.exit(1)
        else:
            log.info('{} TRIED TO KILL ME!!!'.format(message.author))
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
        await client.send_file(ctx.message.channel, path) # , filename=None, tts=False
    else:
        await client.say('You need to provide a user to rate!')


@client.command()
async def echo(*args):
    output = ""
    for word in args:
        output += word
        output += ' '
    await client.say(output)



# ─── VOICE BOT ──────────────────────────────────────────────────────────────────

@client.command(pass_context=True)
async def join(ctx):
    log.info('Joining voice channel.')
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()


# ─── RUN ────────────────────────────────────────────────────────────────────────

client.run(config['discord']['token'])
