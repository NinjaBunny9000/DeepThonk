""" Bot & stream events

Events like the bot booting up and every message that occurs in teh channel 
(event_message) lives here. These are all events with the @bot.event decorator.
 
For more info, check out the TwitchIO library docs:
https://twitchio.readthedocs.io/en/rewrite/twitchio.commands.html#bot
"""

from config.importer import bot, twitch_channel, sign_on_msg, twitch_bot_nick, twitch_team
from utils.logger import loggymclogger as log
from integrations.twitch.api_wrapper import interface
from server_interface import emit_tts

log.debug(f"{__name__} loaded")

team_members = list()
greeted_subscribers = list()


@bot.event
async def event_ready():
    'Called when the bot it booted up.'
    log.info(f"{bot.nick} IS ONLION!!")
    ws = bot._ws
    await ws.send_privmsg(twitch_channel, sign_on_msg)
    global team_members
    team_members = interface.team_members
    # print(twitch_channel) # DEBUG correct
    # print(team_members) # DEBUG correct
    

@bot.event
async def event_raw_data(data):
    interface.monitor_broadcast_state()


@bot.event
async def event_message(ctx):
    global team_members
    global greeted_subscribers
    'Called every message sent in chat. Keep it simple, pls. <3'
    author = ctx.author.name.lower()
    
    # make sure the bot ignores itself
    if author == twitch_bot_nick.lower():
        return
    await bot.handle_commands(ctx)

    # greet/shoutout team members when they say something in chat, 1st time only
    if author in team_members and author != twitch_channel:
        print('TEAM MEMBER DETECTED')
        await emit_tts(f"TEAM MEMBER DETECTED. If you have a sec, follow {author}. I've dropped a link in chat!")
        msg = f"🚨 [{twitch_team}] TEAM MEMBER DETECTED: @{author} => https://twitch.tv/{author}"
        team_members.remove(author)
        await ctx.channel.send(msg)

    # greet subscribers when they enter the chat for first time this stream
    if 'subscriber' in ctx.author.badges and author not in greeted_subscribers and author != twitch_channel: 
        months_subbed = int(ctx.author.tags['badge-info'].split('/')[1])

        greetings = [
            (24, f"📣 @{author} has arrived! They've been supporting for [{months_subbed}] flippin months! ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Slay ninjab1Bigups ninjab1Bigups ninjab1Slay "),
            (12,f"📣 @{author} is BACK! ninjab1Bigups for the continued support of [{months_subbed}] months!"),
            (9, f"📣 @{author} had landed! ninjab1Bigups for the sub babby 👶 and the support of [{months_subbed}] months!"),
            (6, f"📣 @{author} has arrived! Thanks for the [{months_subbed}] months support!"),
            (3, f"📣 @{author} is here! Welcome back! ([{months_subbed}] months of support)"),
        ]

        for month, message in greetings:
            if months_subbed >= month:
                await ctx.channel.send(message)
                break
        
        greeted_subscribers.append(author) # add to list so they're not greeted multiple times
