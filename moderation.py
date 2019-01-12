import asyncio
import time
from conf import twitch_instance
import data_tools
from sfx import play_sfx
import permissions

# config ze bot!
twitch_bot = twitch_instance
 

###################################################################
# SECTION Strike System
###################################################################

# look at all these Globals™
probation_timer = {}    # TODO Move to db
strike_table = {}   # TODO Move to db

@twitch_bot.command('strike')
async def strike(message):
    """
    Command looks like..??? ==> !strike <user> <reason>
    """

    # TODO make a probation timer configurable var in the yaml or content or something
    # TODO check if user is still in room
    # TODO report if they aren't & return
    # TODO handle incorrect usages/token-lengths ????????

    global probation_timer
    global strike_table
    
    # check for permissions
    if not permissions.is_mod(message):
        return

    # tokenize™
    token = data_tools.tokenize(message, 2)
    user = token[1]


    # TODO prevent striking mods
    # can't strike themselves
    if user.lower() == message.author.name.lower():
        msg = 'Ur doin it rong. You can\'t strike mods (or yourself)'
        await twitch_bot.say(message.channel, msg)
        return


    try:
        # if they have 2 stikes or were still on probation
        if time.time() - probation_timer[user] <= 600 or strike_table[user] == 2:
            
            if strike_table[user] == 2:
                msg = 'Strike #3, @{}. Hasta la vista, chump.'.format(user)
                await twitch_bot.say(message.channel, msg)
            else:
                msg = 'Ya dun goof\'d, @{}. Hasta la vista, chump.'.format(user)
                await twitch_bot.say(message.channel, msg)

            # then ban dem
            await twitch_bot.say(message.channel, '/ban {}'.format(user))

            del strike_table[user]
            play_sfx('sfx/nogud.mp3')

        # otherwise this is strike #2
        else:
            if user in strike_table:
                play_sfx('sfx/hooks/question.mp3')
                strike_table.update({user : 2})
                msg = """Strike #2, @{}. Your next strike will result in a ban.
                Please review the Chat Rules, ToS (https://www.twitch.tv/p/legal/terms-of-service/) 
                and Community Guidelines (https://www.twitch.tv/p/legal/community-guidelines/)
                """.format(user)
                await twitch_bot.say(message.channel, msg)
    
    # if this is their first strike, add them to the list
    except KeyError:
        strike_table.update({user : 1})

        # register the time for probation timer
        probation_timer.update({user : time.time()})
        msg = """Strike #1, @{}.  You're on a 10m probationary period. Another strike during this 
                period will result in an immediate and irreversable ban. Please review the 
                Chat Rules, ToS (https://www.twitch.tv/p/legal/terms-of-service/) and 
                Community Guidelines (https://www.twitch.tv/p/legal/community-guidelines/)
            """.format(user)
        play_sfx('sfx/events/strike1.mp3')
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
    
    # check for permissions
    if not permissions.is_mod(message):
        return

    # tokenize™
    token = data_tools.tokenize(message, 1)
    user = token[1]

    try:
        msg = '@{} has {} strikes'.format(user, strike_table[user])
    except:
        msg = 'No strikes for this user.'
        
    await twitch_bot.say(message.channel, msg)


@twitch_bot.command('mybad')
async def mybad(message):
    '!mybad <user> removes a strike for the user.'
    # check for permissions
    if not permissions.is_mod(message):
        return

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
        msg = '@{} isn\'t stoked rn, @{}.'.format(user, message.author.name)


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

# !SECTION 

###################################################################
# SECTION Debug commands (remove in refactor, etc)
###################################################################



# !SECTION 