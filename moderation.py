import asyncio
import time
from conf import twitch_instance
from twitch_chat import tokenize, is_mod
from playsound import playsound

# config ze bot!
twitch_bot = twitch_instance
 
# ze globals
squad_count = 0
troll_count = 0
troll_bans = 0
troll_timeouts = 0
probation_timer = {}
strike_table = {}


@twitch_bot.command('trolls')
async def trolls(message):
    troll_status = "We've seen {} squads, {} shit-tier trolls, and have banned {} lame trolls tonight".format(
        squad_count, troll_count, troll_bans
    )
    await twitch_bot.say(message.channel, troll_status)

@twitch_bot.command('troll')
async def troll(message):
    global squad_count
    global troll_count
    global troll_bans
    global troll_timeouts
    
    token = tokenize(message, 3)
    print(token)

    doin_it_wrong = 'Usage: !troll pban/squad/shitlord. '

    if len(token) == 1:
        await twitch_bot.say(message.channel, doin_it_wrong)
        await asyncio.sleep(3)
        await twitch_bot.say(message.channel, 'Mods, be sure to ban trolls before giving them any \"attention\"')
        return

    if token[1] == 'squad':
        squad_count += 1
        response = 'Shitsquad registered. Whelp. Color-me surprised, we\'ve seen {} tonight.'.format(squad_count)
        await twitch_bot.say(message.channel, response)

    elif token[1] == 'shitlords':
        try:
            troll_count += int(token[2])
            response = 'Shit-tier troll(s) registered. {} so far this stream. We are unimpressed.'.format(troll_count)
            await twitch_bot.say(message.channel, response)
            return
        except:
            usage = '!troll shitlord [qty] when u witnerss sub-par trolling. Git gudder, scrubs.'
            await twitch_bot.say(message.channel, doin_it_wrong + usage)
            return

    elif token[1] == 'timeout':
        if is_mod(message):
            try:
                user = token[2]
                ban_command = '/timeout {} 60'.format(user)
                confirm = 'No problemo, @{}.'.format(message.author.name)
                troll_bans += 1
                await twitch_bot.say(message.channel, confirm)
                if len(token) == 4:
                    ban_reason = token[3]
                    ban_warning = 'Timing out @{} for 1 min. Cuz {}. Say your last words, chump.'.format(user, ban_reason)
                else:
                    ban_warning = 'Timing out @{} in 10s. Say your last words, chump.'.format(user)
                await twitch_bot.say(message.channel, ban_warning)
                await asyncio.sleep(10)
                await twitch_bot.say(message.channel, ban_command)
                rest_in_pepperonis = 'The problem has been taken care of, m\'lady. {} bans so far.'.format(troll_bans)
                await twitch_bot.say(message.channel, rest_in_pepperonis)
                await asyncio.sleep(4)
                memes = '/me tips fedora'
                await twitch_bot.say(message.channel, memes)
                return
            except:
                usage = 'ie, !troll ban [username]. Mods only, meatbags.'
                await twitch_bot.say(message.channel, doin_it_wrong + usage)
                return
        else:
            msg = 'Nice try, chump.'
            await twitch_bot.say(message.channel, msg)
            
    elif token[1] == 'ban':
        if is_mod(message):
            try:
                user = token[2]
                ban_command = '/ban {}'.format(user)
                confirm = 'No problemo, @{}.'.format(message.author.name)
                troll_bans += 1
                await twitch_bot.say(message.channel, confirm)
                if len(token) == 4:
                    ban_reason = token[3]
                    ban_warning = 'Banning @{} in 10s. Cuz {}. Say your last words, chump.'.format(user, ban_reason)
                else:
                    ban_warning = 'Banning @{} in 10s. Say your last words, chump.'.format(user)
                await twitch_bot.say(message.channel, ban_warning)
                await asyncio.sleep(10)
                await twitch_bot.say(message.channel, ban_command)
                rest_in_pepperonis = 'The problem has been taken care of, m\'lady. {} bans so far.'.format(troll_bans)
                await twitch_bot.say(message.channel, rest_in_pepperonis)
                await asyncio.sleep(4)
                memes = '/me tips fedora'
                await twitch_bot.say(message.channel, memes)
                return
            except:
                usage = 'ie, !troll ban [username]. Mods only, meatbags.'
                await twitch_bot.say(message.channel, doin_it_wrong + usage)
                return
        else:
            msg = 'Nice try, chump.'
            await twitch_bot.say(message.channel, msg)


@twitch_bot.command('strike')
async def strike(message):
    """
    Command looks like..??? ==> !strike <user> <reason>
    """

    global probation_timer
    global strike_table
    
    # check for permissions
    if not is_mod(message):
        return

    # tokenize™
    token = tokenize(message, 2)

    user = token[1] 

    # TODO check if user is still in room
        # TODO report if they aren't & return

    # TODO handle incorrect usages/token-lengths ????????

    try:
        # if they have 2 stikes or were still on probation
        if time.time() - probation_timer[user] <= 600 or strike_table[user] == 2:
            
            if strike_table[user] == 2:
                msg = 'Strike #3, @{}. Hasta la vista, chump.'.format(user)
                await twitch_bot.say(message.channel, msg)
            else:
                msg = 'Ya dun goof\'d, @{}. Hasta la vista, chump.'.format(user)
                await twitch_bot.say(message.channel, msg)
            # ban dem
            await twitch_bot.say(message.channel, '/timeout {} 10'.format(user))
            # TODO remove from dictionaries
            await playsound('sfx/nogud.mp3')

        # else add or increment an strike count
        else:
            if user in strike_table:
                # increment
                strike_table.update({user : 2})
                msg = """Strike #2, @{}. Your next strike will result in a ban.
                Please review the Chat Rules, ToS (https://www.twitch.tv/p/legal/terms-of-service/) 
                and Community Guidelines (https://www.twitch.tv/p/legal/community-guidelines/)
                """.format(user)
                await twitch_bot.say(message.channel, msg)
    except KeyError:
        # add them to the list
        strike_table.update({user : 1})
        # start timer
        probation_timer.update({user : time.time()})
        msg = """Strike #1, @{}.  You're on a 10m probationary period. Another strike during this 
                period will result in an immediate and irreversable ban. Please review the 
                Chat Rules, ToS (https://www.twitch.tv/p/legal/terms-of-service/) and 
                Community Guidelines (https://www.twitch.tv/p/legal/community-guidelines/)
            """.format(user)
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('timer')
async def timer(message):
    global probation_timer
    
    # check for permissions
    if not is_mod(message):
        return

    # tokenize™
    token = tokenize(message, 2)
    user = token[1]

    try:
        if time.time() - probation_timer[user] <= 20:
            msg = '@{} still gittin probed'.format(user)
            await twitch_bot.say(message.channel, msg)
        else:
            msg = '@{} not gittin probed (ANYMORE), but has {} strikes.'.format(user, strike_table[user])
            await twitch_bot.say(message.channel, msg)
            await asyncio.sleep(4) # dramatic pause
            await twitch_bot.say(message.channel, '!dundun')
    except KeyError:
        msg = '@{} not gittin probed (YET)'.format(user)
        await twitch_bot.say(message.channel, msg)
        await asyncio.sleep(4) # dramatic pause
        await twitch_bot.say(message.channel, '!dundun')



@twitch_bot.command('strikes')
async def strikes(message):
    global strike_table
    
    # check for permissions
    if not is_mod(message):
        return

    # tokenize™
    token = tokenize(message, 1)
    
    user = token[1]

    try:
        msg = '@{} has {} strikes'.format(user, strike_table[user])
    except:
        msg = 'No strikes for this user.'
        
    await twitch_bot.say(message.channel, msg)

# TODO
@twitch_bot.command('mybad')
async def mybad(message):
    pass
    # check for permissions
    # tokenize™
    # undo

@twitch_bot.command('stroken')
async def stroken(message):
    global strike_table
    
    if strike_table:
        users = '[%s]' % ', '.join(map(str, strike_table.keys()))
        users = users.strip('[]')
        msg = 'Users with 1 or more strikeouts: ' + str(users)
        await twitch_bot.say(message.channel, msg)
    else:
        await twitch_bot.say(message.channel, 'nun be stroked rn fam')

