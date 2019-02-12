import os
import sys

import conf
import integrations.streamelements.api_wrapper
import asyncio
import games.raid
import data_tools

# config ze bot!
twitch_bot = conf.twitch_instance
bigups = {}

async def spammyboi(message): 
    spam_count = 0
    while spam_count < 4:
        spam_count += 1
        await twitch_bot.say(message.channel, 'Spammed {} times!'.format(spam_count))
        await asyncio.sleep(3)

@twitch_bot.command('spammy')
async def spammy(message):
    twitch_bot.loop.create_task(spammyboi(message))


@twitch_bot.command('reboot')
async def restart(message):
    if message.author.mod or message.author.name == conf.streamer:
        await twitch_bot.say(message.channel, 'brb, rebooting...')
        print('Chat-Interrupted')
        print('Stopping the bot..')
        sys.stdout.flush()
        os.execv(sys.executable, ['python'] + sys.argv)
       
    else:
        msg = f"@{message.author.name} tried to kill me! D:"
        print(msg)
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('emoteme')
async def emoteme(message):
    emote_count = 0

    for emote in message.emotes:
        emote_count += 1

    print(f'{emote_count} emotes')


@twitch_bot.command('prefix', unprefixed=False)
async def prefix(message):
    print('WE GUD')


@twitch_bot.command('raidornah')
async def raidornah(message):
    msg = f'raid.start() == {games.raid.start()} // raid.is_happening() == \
    {games.raid.is_happening()}'
    await twitch_bot.say(message.channel, msg)


@twitch_bot.command('team')
async def team(message):
    # reports what team teh sender is on
    chatter = message.author.name
    teams = games.raid.get_team(message)
    msg = f"@{chatter}, you're registered on teh following team(s): {teams}"
    await twitch_bot.say(message.channel, msg)


@twitch_bot.command('raiders')
async def raiders(message):
    # reports what team teh sender is on
    print(games.raid.get_raiders())

@twitch_bot.command('defenders')
async def defenders(message):
    # reports what team teh sender is on
    print(games.raid.get_defenders())


@twitch_bot.command('swapteams')
async def swapteams(message):
    chatter = message.author.name.lower()
    games.raid.swap_teams(chatter)
    teams = games.raid.get_team(message)
    msg = f'@{chatter}, you\'re now on {teams}'
    await twitch_bot.say(message.channel, msg)


@twitch_bot.command('bigups')
async def bigups(message):
    '!bigups <user> <emote>'

    token = data_tools.tokenize(message, 2)
    user = token[1]
    user = data_tools.ats_or_nah(user)
    # global bigups

    # for key, val in bigups.items():
    #     if key == user:
    #         bigups[key] += 1


    msg = f'Bigups for @{user}! What a champ!'
    await twitch_bot.say(message.channel, msg)
    msg = f'ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay ninjab1Slay '
    await twitch_bot.say(message.channel, msg)