""" Bot & stream events

Events like the bot booting up and every message that occurs in teh channel 
(event_message) lives here. These are all events with the @bot.event decorator.
 
For more info, check out the TwitchIO library docs:
https://twitchio.readthedocs.io/en/rewrite/twitchio.commands.html#bot
"""

from config.importer import bot, twitch_channel, sign_on_msg, twitch_bot_nick
from utils.logger import loggymclogger as log

log.debug(f"{__name__} loaded")

@bot.event
async def event_ready():
    'Called when the bot it booted up.'
    log.info(f"{bot.nick} IS ONLION!!")
    ws = bot._ws
    await ws.send_privmsg(twitch_channel, sign_on_msg)


@bot.event
async def event_message(ctx):
    'Called every message sent in chat. Keep it simple, pls. <3'
    
    # make sure the bot ignores itself
    if ctx.author.name.lower() == twitch_bot_nick.lower():
        return
    await bot.handle_commands(ctx)
