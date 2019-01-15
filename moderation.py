import asyncio
import time
import conf
from conf import twitch_instance
import data_tools
from sfx import play_sfx
import privilege

# config ze bot!
twitch_bot = twitch_instance


###############################################################################
# SECTION Reward System
###############################################################################

if conf.moderation['reward_system']:

    @twitch_bot.command('reward')
    async def reward(message):
        """
        Rewards followers/subs with whatever reward currnetly is for the strem.

        !reward <user> <fol/sub>
        """
        # TODO Validation for members in the room

        # global dict for rewards
        reward_register = data_tools.txt_to_list('data/', 'reward_list.txt')
        
        token = data_tools.tokenize(message, 2, lower_case=False)
        
        # if just `!reward`, list people in teh rewards
        if len(token) is 1:
            if len(reward_register) >= 1:
                # list peeps in the cue
                rewardees = data_tools.stringify_list(reward_register, '@')
                msg = f'@{message.author.name}, these rad folks are qeueued for rewards! {rewardees}'
            else:
                msg = f' @{message.author.name}, no community members are queued for rewards (yet).'
            
            await twitch_bot.say(message.channel, msg)
            return

        # spit out how many peeps in teh queue
        if 'qty' == token[1]:
            msg = f'{len(reward_register)} rad dudes in teh queue'
            await twitch_bot.say(message.channel, msg)
            return

        if not privilege.is_mod(message):
            # TODO Drop this into a function that spits out a standard response for lack of priveglage
            msg = f"Sorry, @{message.author.name}, you can't do unless you're as a mod."
            await twitch_bot.say(message.channel, msg)
            return

        # clear the list if rewards rewarded
        if 'clear' == token[1]:
            data_tools.clear_txt('data/', 'reward_list.txt')
            msg = f'Rewards delivered!!! @{message.author.name} cleared the list. Thx for bein rad, dudes!'
            await twitch_bot.say(message.channel, msg)
            return

        # add the person to the list
        else:
            data_tools.add_to_txt('data/','reward_list.txt', token[1]) # new hotness
            # reward_register.append(token[1]) # old and busted
            msg = f'@{token[1]} registered in the reward cue!'
            await twitch_bot.say(message.channel, msg)

# !SECTION 



###################################################################
# SECTION Strike System
###################################################################

if conf.moderation['strike_system']:

    # look at all these Globals™
    probation_timer = {}    # TODO Move to db
    strike_table = {}   # TODO Move to db

    @twitch_bot.command('strike')
    async def strike(message):
        'Command looks like..??? ==> !strike <user> <reason>'

        # TODO make a probation timer configurable var in the yaml or content or something
        # TODO check if user is still in room
        # TODO report if they aren't & return
        # TODO handle incorrect usages/token-lengths ????????

        global probation_timer
        global strike_table
        
        # check for privilege
        if not privilege.is_mod(message):
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
            if time.time() - probation_timer[user] <= conf.moderation['strike_timeout']*60 or strike_table[user] == 2:
                
                if strike_table[user] == 2:
                    msg = f'Strike #3, @{user}. Hasta la vista, chump.'
                    await twitch_bot.say(message.channel, msg)
                else:
                    msg = f'Ya dun goof\'d, @{user}. Hasta la vista, chump.'
                    await twitch_bot.say(message.channel, msg)

                # then ban dem
                await twitch_bot.say(message.channel, f'/ban {user}')

                del strike_table[user]
                play_sfx('sfx/nogud.mp3')

            # otherwise this is strike #2
            else:
                if user in strike_table:
                    play_sfx('sfx/hooks/question.mp3')
                    strike_table.update({user : 2})
                    await twitch_bot.say(message.channel, f'/timeout {conf.strike_timeout[1]} {user}')
                    msg = f'Strike #2, @{user}. Your next strike will result in a ban.'
                    await twitch_bot.say(message.channel, msg)
        
        # if this is their first strike, add them to the list
        except KeyError:
            strike_table.update({user : 1})

            # register the time for probation timer
            probation_timer.update({user : time.time()})
            # time them out
            await twitch_bot.say(message.channel, f'/timeout {conf.strike_timeout[0]} {user}')
            msg = f"""Strike #1, @{user}.  You're on a 10m probationary period. Another strike during this 
                    period will result in an immediate and irreversable ban.
                """
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

# !SECTION 

###################################################################
# SECTION Debug commands (remove in refactor, etc)
###################################################################



# !SECTION 