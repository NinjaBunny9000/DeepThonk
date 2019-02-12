import time

import conf
import data_tools

from integrations.twitch import privilege
from sfx.sfx import play_sfx, play_random


# config ze bot!
twitch_bot = conf.twitch_instance

###############################################################################
# ANCHOR  Strike System
###############################################################################

# look at all these Globals™
probation_timer = {}    # TODO Move to db
strike_table = dict()   # TODO Move to db

@twitch_bot.command('strike')
async def strike(message):
    'Command looks like..??? ==> !strike <user> <reason>'

    # TODO make a probation timer configurable var in the yaml or content or something

    global probation_timer
    global strike_table

    strike_timeout = conf.moderation['strike_timeout']
    probation_period = conf.moderation['probation_period']

    # check for privilege
    if not privilege.is_mod(message):
        return

    # tokenize™
    token = data_tools.tokenize(message, 2)
    try:
        user = token[1]
    except IndexError:
        msg = f'Try !strik <user> or !stroken for a list of currently stroked individuals.'
        await twitch_bot.say(message.channel, msg)
        return

    user = data_tools.ats_or_nah(user)

    # TODO prevent striking mods
    # stop hitting yourself
    if user.lower() == message.author.name.lower() or privilege.is_mod(user):
        msg = 'Ur doin it rong. You can\'t strike mods (or yourself)'
        await twitch_bot.say(message.channel, msg)
        return

    try:
        # if they have 2 stikes or were still on probation
        if time.time() - probation_timer[user] <= probation_period or strike_table[user] == 2:
            strike_3_message = conf.moderation['strike_3_message']
            if strike_table[user] == 2:
                msg = f'Strike #3, @{user}. {strike_3_message}'
                await twitch_bot.say(message.channel, msg)
            else:
                msg = f'Ya dun goof\'d, @{user}. {strike_3_message}'
                await twitch_bot.say(message.channel, msg)

            # then ban dem
            await twitch_bot.say(message.channel, f'/ban {user}')

            del strike_table[user]
            play_random('sfx/events/strikes/')

        # otherwise this is strike #2
        else:
            if user in strike_table:
                play_random('sfx/events/strikes/')
                strike_table.update({user : 2})
                await twitch_bot.say(
                    message.channel, 
                    f'/timeout {strike_timeout}m {user} like shit-tier, but shittier.')
                strike_2_message = conf.moderation['strike_2_message']
                msg = f'Strike #2, @{user}. {strike_2_message}'
                await twitch_bot.say(message.channel, msg)
    
    # if this is their first strike, add them to the list
    except KeyError:
        strike_table.update({user : 1})

        # register the time for probation timer
        probation_timer.update({user : time.time()})
        # time them out
        await twitch_bot.say(
            message.channel, 
            f'/timeout {strike_timeout}m {user} cuz shit-tier.')
        strike_1_message = conf.moderation['strike_1_message']
        msg = f'Strike #1, @{user}.  {strike_1_message}'
        play_random('sfx/events/strikes/')
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('strikes')
async def strikes(message):
    """
    !Strike <user>

    1st = 10m probationary period
    2nd = Instaban if still in prob period
    3rd = Immediate ban
    """
    global strike_table
    
    # check for privilege
    if not privilege.is_mod(message):
        return

    # tokenize™
    token = data_tools.tokenize(message, 1)
    user = token[1]

    try:
        msg = f'@{user} has {strike_table[user]} strikes'
    except:
        msg = 'No strikes for this user.'
        
    await twitch_bot.say(message.channel, msg)


@twitch_bot.command('mybad')
async def mybad(message):
    '!mybad <user> removes a strike for the user.'
    # check for privilege
    if not privilege.is_mod(message):
        return

    global strike_table

    token = data_tools.tokenize(message, 1)    # tokenize™

    # return fyi if no user provided
    if len(token) == 1:
        msg = 'Ur doin it rong. Try !mybad <user>.'
        await twitch_bot.say(message.channel, msg)
        return
    
    user = token[1]

    # TODO prevent striking mods
    # can't strike themselves
    if user.lower() == message.author.name.lower():
        msg = 'Ur doin it rong. You can\'t strike mods (or yourself)'
        await twitch_bot.say(message.channel, msg)
        return

    try:
        # if they've got 2 strikes, remove 1
        if user in strike_table and strike_table[user] == 2:
            strike_table[user] = 1

        # if they only have 1, then delete them
        else:
            del strike_table[user]

        msg = 'dun'
        await twitch_bot.say(message.channel, msg)

    except KeyError:
        msg = f'@{user} isn\'t stoked rn, @{message.author.name}.'


@twitch_bot.command('stroken', alias=('yoted', 'yuted', 'yoten'))
async def stroken(message):
    global strike_table
    
    if strike_table:
        users = '[%s]' % ', '.join(map(str, strike_table.keys()))
        users = users.strip('[]')
        msg = 'Yuted users: ' + str(users)
        await twitch_bot.say(message.channel, msg)
    else:
        await twitch_bot.say(message.channel, 'nun be stroked rn fam')