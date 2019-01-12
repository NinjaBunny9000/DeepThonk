import conf
from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
from cah import play_hand
from haveyouever import have_you_tho
import sys
import os
import db_insert
import db_query 
import random
import content
import asyncio
from twitch_permissions import is_bot, is_mod
import games
from playsound import playsound
from games import raid_event, raid_in_progress, keep_score, reset_emote_count, keep_oop_score, deal_damage
import data_tools
from sfx import play_sfx


# config ze bot!
twitch_bot = twitch_instance
welcome_msg_sent = 0

# globals everyone can bitch about (that are actually just db objects in testing)
band_names = []
branch_url = 'https://github.com/NinjaBunny9000/DeepThonk/tree/raid-game' # TODO move to db
repo_url = 'https://github.com/NinjaBunny9000/DeepThonk/'
# time_users_last_polled = time.now()
               
def update_task_at_launch():
    task = db_query.get_latest_task()
    f = open('data\\task.txt', 'w+')
    f.write('!task = {}'.format(task.description))
    f.close()

update_task_at_launch()



# ─── WELCOME MESSAGE ────────────────────────────────────────────────────────────

@twitch_bot.override
async def raw_event(message):
    global welcome_msg_sent
    if not welcome_msg_sent:
        welcome_msg_sent = 1
        print(conf.bot_name().capitalize() + ' has landed.')
        await twitch_bot.say(twitch_channel(), welcome_msg())
        await twitch_bot.say(twitch_channel(), "/me tips hat to chat")

        # make initial list of people in the room
        games.update_defenders_list()
        msg = '{} defenders registered.'.format(games.get_def_count())
        await twitch_bot.say(twitch_channel(), msg)
        

@twitch_bot.override
async def event_user_join(user):
    # print(user.name)
    # if raid is happening
    if games.raid_start():
        # add new people that join to the attacking team
        games.append_raiders(user)
    else:
        games.append_defenders(user)


@twitch_bot.override
async def event_user_leave(user):
    # print(user.name)
    pass
    # if raid is happening
    # if games.raid_start():
        # add new people that join to the attacking team

    


# ─── PLAIN OLE FUNCTIONS ────────────────────────────────────────────────────────

def parse_commands(message, parts): 
    message_parts = message.content.split(' ', parts)
    return message_parts

 
def display_task_on_obs(task):
    f = open('data\\task.txt', 'w+')
    f.write('!task = {}'.format(task))
    f.close()


def shuffle_msg(msg_list):
    """
    Takes a list of responses (if more than one) and shuffles them and combines them
    so that they can all be sent in one message. ex: Oi deepthonk! Do you like dicks?
    """
    random.shuffle(msg_list)
    return ' '.join(msg_list)


def tokenize(message, parts=0):
    if parts == 0:
        return message.content.lower().split(' ') # TOKENIZE™
    else: 
        return message.content.lower().split(' ', parts) # TOKENIZE™


def stringify_list(stupid_list, prefix_char=''):
    'Takes a list and concats into a string, separated by commas, with (or without) prefix arg.'
    addy_part = ', {}'.format(prefix_char)
    stringificated_listymajig =  '[%s]' % addy_part.join(map(str, stupid_list))
    stringificated_listymajig = stringificated_listymajig.strip('[]')
    stringificated_listymajig = prefix_char + stringificated_listymajig
    return stringificated_listymajig


# TODO  Placeholder for db-like functionality, storing lists to txt
def list_to_file():
    pass

# TODO  Placeholder for db-like functionality, reading lists from txt
def read_list_from_file():
    pass


# ─── HELP MENU ──────────────────────────────────────────────────────────────────

@twitch_bot.command(
    'cmd', 
    alias=['command', 'commands', 'help', 'wtf', 'wth'],
    desc='Get help info about the bot'
    )
async def cmd(message):
    await twitch_bot.say(message.channel, content.help_menu(message))


# ─── TRADITIONAL COMMANDS - VIA @COMMANDS ───────────────────────────────────────
  
@twitch_bot.command('bands')
async def bands(message):
    """
    Works similar to quotes, but tracks TOTALLY AWESOME band names. Still a WIP, 
    needs to connect to the database, that kind of stuff.
    """
    message_parts = parse_commands(message, 2)

    if len(message_parts) >= 2:
        subcmd = message_parts[1]

        if subcmd == 'add' and is_mod(message):
            band_names.append(message_parts[2])
            msg = '{} added to the list of TOTALLY AWESOME band names.'.format(message_parts[2])
            await twitch_bot.say(message.channel, msg)

        elif subcmd == 'oops' and is_mod(message):
            band_names.pop()
            await twitch_bot.say(message.channel, 'Last band name removed. Who dun fucked up this time?!???')
        
        elif subcmd == 'clear' and is_mod(message):
            band_names.clear()
            await twitch_bot.say(message.channel, 'No clue why you did this, but all the band names are GONE!.. Jerk! D:')
        
        elif not is_mod(message):
            await twitch_bot.say(message.channel, 'Y u do dat?! Where\'s your sword, pal?')

        else:
            await twitch_bot.say(message.channel, 'Syntax tip: !bands add/list/clear')

    else:
        if len(band_names) == 0:
            await twitch_bot.say(message.channel, 'No bands in the list!')
        else:
            bands = '[%s]' % ', '.join(map(str, band_names))
            bands = bands.strip('[]')
            msg = 'Here\'s some totally awesome band names: {}'.format(bands)
            await twitch_bot.say(message.channel, msg)


@twitch_bot.command('task')
async def task(message):
    """
    Keep track of what task you're currently workin on during stream. (WIP: needs to
    connect to db)
    """
    message_parts = parse_commands(message, 1)

    if len(message_parts) >= 2 and is_mod(message):
        current_task = str(message_parts[1])[:250]  # update the current task
        db_insert.add_task(current_task)
        # TODO call this at launch, too
        display_task_on_obs(current_task)
        await twitch_bot.say(message.channel, 'Task updated')
    
    else:
        msg = 'Current task: {}'.format(db_query.get_latest_task())
        await twitch_bot.say(message.channel, msg) # print the current task


@twitch_bot.command('randomtask')
async def randomtask(message):
    await twitch_bot.say(message.channel, str(db_query.rand_task())) # print the current task


@twitch_bot.command('cah')
async def cah(message):
    """
    Cards against humanity play-generator.
    """
    await twitch_bot.say(message.channel, play_hand())


@twitch_bot.command('easteregg')
async def easteregg(message):
    """
    Just an easter egg.
    """
    await twitch_bot.say(message.channel, content.easter_egg(message))


@twitch_bot.command('hye')
async def haveyou(message):
    """
    Have you ever []??? Legitimate questions only.
    """
    #! function is disabled for now:
    await twitch_bot.say(message.channel, content.function_disabled())
    # message_parts = parse_commands(message, 1)

    # if len(message_parts) >= 2 and is_mod(message):
    #     db_insert.add_hye(str(message_parts[1]), message.author.name)
    #     await twitch_bot.say(
    #         message.channel,
    #         '{} added: "Have you ever {}?"'.format(message.author.name, message_parts[1])
    #         )

    # else:
    #     msg = 'Have you ever ' + db_query.rand_hye().item + '?'
    #     await twitch_bot.say(message.channel, msg) # print the current task


@twitch_bot.command('reward')
async def reward(message):
    """
    Rewards followers/subs with whatever reward currnetly is for the strem.

    !reward <user> <fol/sub>
    """
    # TODO Validation for members in the room

    # global dict for rewards
    reward_register = data_tools.txt_to_list('data/', 'reward_list.txt')
    
    token = tokenize(message, 2)

    
    # if just `!reward`, list people in teh rewards
    if len(token) is 1:
        if len(reward_register) >= 1:
            # list peeps in the cue
            rewardees = stringify_list(reward_register, '@')
            msg = '@{}, these rad folks are qeueued for rewards! {}'.format(message.author.name, rewardees)
        else:
            msg = ' @{}, no community members are queued for rewards (yet).'.format(message.author.name)
        
        await twitch_bot.say(message.channel, msg)
        return

    # spit out how many peeps in teh queue
    if 'qty' == token[1]:
        msg = '{} rad dudes in teh queue'.format(len(reward_register))
        await twitch_bot.say(message.channel, msg)
        return

    if not is_mod(message):
        # TODO Drop this into a function that spits out a standard response for lack of priveglage
        msg = "Sorry, @{}, you can't do unless you're as a mod.".format(message.author.name)
        await twitch_bot.say(message.channel, msg)
        return

    # clear the list if rewards rewarded
    if 'clear' == token[1]:
        data_tools.clear_txt('data/', 'reward_list.txt')
        msg = 'Rewards delivered!!! @{} cleared the list. Thx for bein rad, dudes!'.format(message.author.name)
        await twitch_bot.say(message.channel, msg)
        return

    # add the person to the list
    else:
        data_tools.add_to_txt('data/','reward_list.txt', token[1]) # new hotness
        # reward_register.append(token[1]) # old and busted
        msg = '@{} registered in the reward cue!'.format(token[1])
        await twitch_bot.say(message.channel, msg)





# ─── OVERRIDE ───────────────────────────────────────────────────────────────────

@twitch_bot.override
async def event_message(message):
    """
    Each message in chat is sent through this command. Parse teh data (into tokens, ofc),
    add a conditional or two, and make all sorts of fun stuff happen!
    """
    # prevent bot from responding to itself
    if message.author.name == twitch_bot.nick:
        return

    # ignore certain users
    if message.author.name in conf.ignore_list:
        return

    # enable bot.commands stuffs to werk
    await twitch_bot.parse_commands(message)

    # msg = ''
    multi_msg = list()  # creates an empty list for messages to get shuffled and responded with
    message_parts = tokenize(message)  # TOKENIZE™
    mod = is_mod(message)
    bot = conf.bot_name().lower()

    if 'take a nap' in message.content.lower() and bot in message.content.lower() and mod:
        """
        Demonstrate the stubborness of your robit.
        """
        await twitch_bot.say(message.channel, '/me yawns')
        await twitch_bot.say(message.channel, 'maybe later, @{}'.format(message.author.name))
        return

    # return FAQ's
    if content.faq(message):
        msg = content.faq(message)
        await twitch_bot.say(message.channel, msg)


# ─── RAID REACT ─────────────────────────────────────────────────────────────────
    """
    Considerations:
    - on_message loop happens every message
    - Can't talk to twitch chat (use await) within function called here.

    IDEA 1: Report hp ever x-hp. Would require using the on_message loop
    and some logic and/or conditionals to report only losing team, etc.

    IDEA 2: Incorporate into timed-out raid react. This happens in games.py
    and includes async sleep functions (timeouts). Could be not fun, but 
    would have control over reporting health ever x-seconds.

    """

    # update the viewer list for defending
    # TODO How to make this happen all cached and stuff? 
    # games.update_defenders_list()

    if games.raid_is_happening():


        # send commands periodically (@jigo has async solution)
        # FIXME this wont work because loop only happens once per message sent

        # count & score emotes
        if message.emotes:   

            deal_damage(message)

            print('raiding.hp={} || defending.hp={}'.format(
                games.raiding.hp, games.defending.hp
                ))

            # prints hp to .txt file
            data_tools.score_to_txt(games.defending.hp, games.raiding.hp)

            # WIN CONDITION
            if games.report_ko():
                # end raid & reset the scores
                games.end_raid()

                raid_winner = games.get_winner() 
                
                play_sfx('sfx/events/raid_victory.mp3')

                # report the victor
                msg = 'Raid over! The winner is {}'.format(raid_winner)
                await twitch_bot.say(message.channel, msg)

    
            # # hp report conditions met?
            # if games.hp_condition():
            #     # report hp
            #     msg = '{} is below 50% health!'.format(games.hp_condition())
            #     await twitch_bot.say(message.channel, msg)



# ─── SILLY STUFF ────────────────────────────────────────────────────────────────

    # mock links that people send
    if (any(s in message.content.lower() for s in ('http://','https://','www.'))) and (not is_mod(message) or not is_bot(message)):
        await twitch_bot.say(message.channel, 'NSFW!!')

    # respond if sentient
    if any(s in message.content.lower() for s in ('sentient.','sentient!','sentient?','sentient')):
        await twitch_bot.say(message.channel, content.sentient(message))

    # respond if sentient
    if 'i have a question'.lower() in message.content.lower():
        playsound('sfx/hooks/question.mp3')
        return


# ─── WHEN BOT IS DIRECTLY ADDRESSED ─────────────────────────────────────────────

    # don't be a wanker
    elif 'oi' in message_parts[0] and bot in message_parts:
        await twitch_bot.say(message.channel,'oi bruv!')
    
    # cuz your bot is from Texas
    elif 'howdy' in message_parts[0]:
        await twitch_bot.say(message.channel, 'Howdy, @{}!'.format(message.author.name))

    # for use by Robosexuals™ only!
    elif 'love me' in message.content.lower() and bot in message.content.lower():
        multi_msg.append(content.binary_responses() + ', @{}.'.format(message.author.name))
    
    # handles when the bot is mentioned/adressed in a message, or asked a question
    elif message.content.lower().startswith(bot):
        if len(message_parts) > 1:
            if message.content[-1] is '?':
                multi_msg.append(content.binary_responses() + ', @{}.'.format(message.author.name))
            elif message.content[-1] is '.': 
                multi_msg.append(content.generic_responses(message))
            elif message.content[-1] is '!':
                multi_msg.append(content.stop_yelling_at_me()) # pls do not D:
            else:
                multi_msg.append(content.generic_responses(message))
        elif message.content[-1] is '?': 
            multi_msg.append('wot?? 0_o')
        elif message.content[-1] is '!': 
            multi_msg.append('wot!?!!! o_0')
        else:
            multi_msg.append('yea?')    
    
    elif len(message_parts) > 1 and message_parts[-1] == bot + '?':
        multi_msg.append(content.binary_responses() + ', @{}.'.format(message.author.name))
    elif len(message_parts) > 1 and message_parts[-1] == bot + '!':
        multi_msg.append(content.generic_responses(message))
    elif len(message_parts) > 1 and message_parts[-1] == bot:
        multi_msg.append(content.generic_responses(message))

    
# ─── CALL + RESPONSES ───────────────────────────────────────────────────────

    # responses to random words and shit. customize in content.py
    msg = content.get_response_to_call(message)
    if msg is not None:
        multi_msg.append(msg)
            
    # the circular argument
    if 'buddy' and r'\s?(buddy)[\W$]' in message.content.lower():
        multi_msg.append('@{} - I ain\'t your buddy, friend!'.format(message.author.name))
    elif 'friend' and r'\s?(friend)[\W$]' in message.content.lower():
        multi_msg.append('@{} - I ain\'t your friend, guy!!'.format(message.author.name))
    elif 'guy' and r'\s?(guy)[\W$]' in message.content.lower():
        multi_msg.append('@{} - I ain\'t your guy, buddy!!'.format(message.author.name))

    # who said robit?     
    if any(s in message_parts for s in ('robot','robit','bot')):
        multi_msg.append(content.someone_sed_robit())

    # sometimes you just wanna feel loved
    if (any(s in message.content.lower() for s in ('love you','love u')) and bot):
        multi_msg.append(content.love_or_nah())
      

    # Combine all responses in a random order and send them in chat
    if multi_msg:
        reply = shuffle_msg(multi_msg)
        # print('reply: ' + reply)
        await twitch_bot.say(message.channel, reply.strip("\n"))

    # sum1 sed fortnite
    if 'play' in message.content.lower() and 'fortnite' in message.content.lower():
        msg = 'y would u even think that, @{}??'.format(message.author.name)
        await twitch_bot.say(message.channel, msg)
        await twitch_bot.say(message.channel,'/timeout {} 30'.format(message.author.name))

    elif 'fortnite' in message.content.lower():
        msg = 'who sed fortnite!?!!??...'
        await twitch_bot.say(message.channel, msg)
        await twitch_bot.say(message.channel,'/timeout {} 15'.format(message.author.name))


   
# ─── AUF ODER AUS ───────────────────────────────────────────────────────────────

    # when it's past the bot's bed time
    if 'say goodnight' in message.content.lower() and bot in message.content.lower() and is_bot_admin:
        multi_msg.append('goodnight, everyone!!')

    if  message.content.lower().startswith("goodnight, " + bot) and message.author.name == streamer():
        await twitch_bot.say(message.channel, content.last_words())
        bot = conf.twitch_instance
        print('Chat-Interrupted')
        print('Stopping the bot..')
        bot.stop(exit=True)
        
    if ('goodnight' in message.content.lower() or 'gnight' in message.content.lower()) and bot in message.content.lower():
        multi_msg.append('goodnight, {}!'.format(message.author.name))

    # make it stahp
    if 'stahp' in message.content.lower() and (message.author.name == streamer() or message.author.name == 'jigokuniku') :
        await twitch_bot.say(message.channel, content.last_words())
        bot = conf.twitch_instance
        print('Chat-Interrupted')
        print('Stopping the bot..')
        bot.stop(exit=True)


# stops the bot from Twitch chat command !die
@twitch_bot.command('quit')
async def quit(message):
    if message.author.mod or message.author.name == streamer():
        await twitch_bot.say(message.channel, content.last_words())  # DEBUG comment later (used for debug)
        bot = conf.twitch_instance
        print('Chat-Interrupted')
        print('Stopping the bot..')
        bot.stop(exit=True)
       
    else:
        msg = "@{user} tried to kill me! D:".format(user=message.author.name)
        print(msg)
        await twitch_bot.say(message.channel, msg)


###################################################################
# SECTION MENUS & Other Useful Info
###################################################################

# REVIEW these got moved to content.py by way of event_message in twitch_chat.py

# @twitch_bot.command('theme')
# async def theme(message):
#     msg = "The theme Bun uses is Material Ocean High Contrast, with some modifications: https://imgur.com/a/ivJByy2"
#     await twitch_bot.say(message.channel, msg)


# @twitch_bot.command('editor', alias=['ide'])
# async def editor(message):
#     msg = "The editor Bun uses is VSCode: https://code.visualstudio.com/"
#     await twitch_bot.say(message.channel, msg)


# @twitch_bot.command('git', alias=['versioning', 'github'])
# async def git(message):
#     msg = "Bun's github is: https://github.com/NinjaBunny9000"
#     await twitch_bot.say(message.channel, msg)


# @twitch_bot.command('toolset', alias=['workflow'])
# async def toolset(message):
#     msg = "Bun's using VSCode on Windows right now. !theme !git !branch !font for more info."
#     await twitch_bot.say(message.channel, msg)

# @twitch_bot.command('steam')
# async def steam(message):
#     msg = "Add Bun on Steam! https://steamcommunity.com/id/ninjabunny9000/"
#     await twitch_bot.say(message.channel, msg)


# @twitch_bot.command('font')
# async def font(message):
#     msg = "Bun uses Fira Code with font ligatures. https://github.com/tonsky/FiraCode"
#     await twitch_bot.say(message.channel, msg)


@twitch_bot.command('branch', alias=['current'])
async def branch(message):
    token = tokenize(message, 1)
    global branch_url
    
    if is_mod(message) and len(token) == 2:
        # !branch <url> ==> token[0] token[1]
        branch_url = token[1]
        msg = 'New branch set to \"{}\"'.format(branch_url)
        await twitch_bot.say(message.channel, msg)
    else:
        msg = "The branch Bun's working in rn is: {}".format(branch_url)
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('repo', alias=['repository', 'suppository'])
async def repo(message):
    token = tokenize(message, 1)
    global repo_url
    
    if is_mod(message) and len(token) == 2:
        # !repo <url> ==> token[0] token[1]
        repo_url = token[1]
        msg = 'New project repo set to \"{}\"'.format(repo_url)
        await twitch_bot.say(message.channel, msg)
    else:
        msg = "The repo Bun's working with rn is: {}".format(repo_url)
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('shoutout')
async def shoutout(message):
    if is_mod(message):
        msg_parts = parse_commands(message, 2)
        try:
            msg = "Big ups to @{}! They're a friend of the stream and worth a follow, if you have the time! https://twitch.tv/{}".format(msg_parts[1], msg_parts[1])
            await twitch_bot.say(message.channel, msg)
        except:
            msg = "You didn't include a streamer to shout out to, {}.".format(message.author.name)
            await twitch_bot.say(message.channel, msg)


# @twitch_bot.command('kanban')
# async def kanban(message):
#     msg = "https://trello.com/b/Fm4Q3mBx/ninjabunny9000-stream-stuffs"
#     await twitch_bot.say(message.channel, msg)


# @twitch_bot.command('portfolio')
# async def portfolio(message):
#     msg = "Bun's portfolio is online @ www.ninjabunny9000.com (under construction)"
#     await twitch_bot.say(message.channel, msg)


# @twitch_bot.command('bmo')
# async def bmo(message):
#     msg = "https://imgur.com/gallery/LhPlY"
#     await twitch_bot.say(message.channel, msg)


# @twitch_bot.command('chasers')
# async def chasers(message):
#     msg = "SVL are GREAT folks! Here's a link to the team's streams. https://www.twitch.tv/team/stormviewlive - Tell them @NinjaBunny9000 sent ya & show em some love! <3"
#     await twitch_bot.say(message.channel, msg)


# @twitch_bot.command('docs')
# async def docs(message):
#     msg = "Rn, Bun's updating https://github.com/NinjaBunny9000/DeepThonk/blob/doc-updates/README.md"
#     await twitch_bot.say(message.channel, msg)


# !SECTION 


# ─── DEBUG COMMANDS ─────────────────────────────────────────────────────────────


# REVIEW Purge these during the next refactor 

@twitch_bot.command('debug')
async def debug(message):
    """
    DEBUG: change msg var to print whatever var u tryin'a lern gooder
    """
    msg = conf.bot_name().lower()   
    await twitch_bot.say(message.channel, msg)


@twitch_bot.command('author')
async def author(message):
    await twitch_bot.say(message.channel, str(message.author.id))


@twitch_bot.command('subornah')
async def subornah(message):
    await twitch_bot.say(message.channel, str(message.author.subscriber))


@twitch_bot.command('channel')
async def channel(message):
    await twitch_bot.say(message.channel, str(message.channel.id))


@twitch_bot.command('viewers')
async def viewers(message):
    print(twitch_bot.viewers)
    print(twitch_bot.viewers["#" + message.channel])
    print(twitch_bot.channel_stats)
    print(twitch_bot.hosts)
    print(twitch_bot.host_count)


@twitch_bot.command('register')
async def register(message):
    """
    Registers a Twitch user with a service-agnostic ID in the database. WIP, mostly used
    for debugging at the moment.
    """
    if db_insert.add_user_twitch(message):
        msg = 'Registered!'
    else:
        msg = 'You already registered!'
    await twitch_bot.say(message.channel, msg)


@twitch_bot.command('botmod')
async def botmod(message):
    """
    Checks if user calling is a bot mod or not.
    """
    msg = 'Usage: !botmod, !botmod [user], or !botmod [user] [true/false]'
    message_parts = message.content.lower().split(' ')  # TOKENIZE™
    arg_count = len(message_parts)
    if arg_count == 1:
        if db_query.is_bot_mod_twitch(message.author.name):
            msg = 'You are a Bot Mod!'
        else:
            msg = 'You are NOT a Bot Mod!'
    elif arg_count == 2:
        if db_query.is_bot_mod_twitch(message_parts[1]):
            msg = '{} is a Bot Mod!'.format((message_parts[1]))
        else:
            msg = '{} is a NOT Bot Mod!'.format((message_parts[1]))
    elif arg_count == 3:
        # TODO: Verify user calling is a bot mod, themselves
        if message_parts[2] =='true':
            msg = db_query.set_bot_mod_twitch(message_parts[1], True)
        elif message_parts[2] =='false':
            msg = db_query.set_bot_mod_twitch(message_parts[1], False)
    
    await twitch_bot.say(message.channel, msg)


# list commands registered with the async library
@twitch_bot.command('listcommands')
async def listcommands(message):
    commands = list(twitch_bot.commands.keys())
    print(commands)
    # await twitch_bot.say(message.channel, twitch_bot.commands)





