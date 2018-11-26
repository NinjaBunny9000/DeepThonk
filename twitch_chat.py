import conf
from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
from cah import play_hand
from playsound import playsound
from haveyouever import have_you_tho
import sys
import os
import db_insert
import db_query
import random
import content
import asyncio


# config ze bot!
twitch_bot = twitch_instance

band_names = []
current_task = 'None.'
welcome_msg_sent = 0


# ─── WELCOME MESSAGE ────────────────────────────────────────────────────────────

@twitch_bot.override
async def raw_event(message):
    global welcome_msg_sent
    if not welcome_msg_sent:
        welcome_msg_sent = 1
        print(conf.bot_name().capitalize() + ' has landed.')
        await twitch_bot.say(twitch_channel(), welcome_msg())
        await twitch_bot.say(twitch_channel(), "/me tips hat to chat")


# ─── PLAIN OLE FUNCTIONS ────────────────────────────────────────────────────────

def parse_commands(message, parts): 
    message_parts = message.content.split(' ', parts)
    return message_parts

 
def is_mod(message):
    if (message.author.mod or message.author.name.lower() == streamer().lower()):
        return True
    else:
        return False

 
def is_bot(message):
    if (message.author.name.lower() in str(conf.bot_list).lower()):
        return True
    else:
        return False


def shuffle_msg(msg_list):
    """
    Takes a list of responses (if more than one) and shuffles them and combines them
    so that they can all be sent in one message. ex: Oi deepthonk! Do you like dicks?
    """
    random.shuffle(msg_list)
    return ' '.join(msg_list)


def change_scene(scene):
    """
    **Requires 'Advance Scene Switcher' plug-in**
    Swap scenes in OBS studio by writing the scene name to a file.
    """
    f = open('scene_next.txt', 'w+')
    f.write(scene)
    f.close()

def get_scene():
    """
    **Requires 'Advance Scene Switcher' plug-in**
    Read current scene from OBS studio, which is writing scene names 
    to a .txt file.
    """
    f = open('scene_current.txt', 'r+')
    scene = f.readline()
    f.close()
    return scene


# ─── HELP MENU ──────────────────────────────────────────────────────────────────

@twitch_bot.command('cmd', 
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

    global current_task

    if len(message_parts) >= 2 and is_mod(message):
        current_task = str(message_parts[1])  # update the current task
        await twitch_bot.say(message.channel, 'Task updated')
    
    else:
        msg = 'Current task: {}'.format(current_task)
        await twitch_bot.say(message.channel, msg) # print the current task


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

@twitch_bot.command('theme')
async def theme(message):
    msg = "The theme Bun uses is Material Ocean High Contrast, with some modifications: https://imgur.com/a/ivJByy2"
    await twitch_bot.say (message.channel, msg)

@twitch_bot.command('editor')
async def editor(message):
    msg = "The editor Bun uses is VSCode: https://code.visualstudio.com/"
    await twitch_bot.say (message.channel, msg)

@twitch_bot.command('shoutout')
async def shoutout(message):
    if is_mod(message):
        msg_parts = parse_commands(message, 2)
        try:
            msg = "Big ups to @{}! They're a friend of the stream and worth a follow, if you have the time!".format(msg_parts[1])
            await twitch_bot.say(message.channel, msg)
        except:
            msg = "You didn't include a streamer to shout out to, {}.".format(message.author.name)
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
    message_parts = message.content.lower().split(' ')  # TOKENIZE™
    mod = is_mod(message)
    bot = conf.bot_name().lower()

    if 'take a nap' in message.content.lower() and bot in message.content.lower() and mod:
        """
        Demonstrate the stubborness of your robit.
        """
        await twitch_bot.say(message.channel, '/me yawns')
        await twitch_bot.say(message.channel, 'maybe later, @{}'.format(message.author.name))
        return


# ─── SILLY STUFF ────────────────────────────────────────────────────────────────

    # mock links that people send
    if (any(s in message.content.lower() for s in ('http://','https://','www.'))) and (not is_mod(message) or not is_bot(message)):
        await twitch_bot.say(message.channel, 'NSFW!!')

    # respond if sentient
    if any(s in message.content.lower() for s in ('sentient.','sentient!','sentient?','sentient')):
        await twitch_bot.say(message.channel, content.sentient(message))


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


# ─── SFX ────────────────────────────────────────────────────────────────────────

@twitch_bot.command('slideup')
async def slideup(message):
    await playsound('sfx/slideup.mp3')


# ─── SCENE SWITCHER ─────────────────────────────────────────────────────────────

@twitch_bot.command('scene')
async def scene(message):
    if is_mod(message):
        scene = get_scene()
        msg = '@{}, the current scene is {}'.format(message.author.name, scene)
        await twitch_bot.say(message.channel, msg)

    
@twitch_bot.command('raid')
async def raid(message):
    if is_mod(message):
        await asyncio.sleep(4)
        await twitch_bot.say(message.channel, "!redalert")  # RED LIGHTS

        await asyncio.sleep(5)  # 9s BSOD
        change_scene('TECHNICAL DIFFICULTIES')
        
        await asyncio.sleep(6)  # 15s
        msg = 'ATTENTION, NINJAS! We\'ve been RAIDED! Our networks are vulnerable!!'
        await twitch_bot.say(message.channel, msg)
        
        await asyncio.sleep(10)  # 25s Switch to HackerTyper
        change_scene('RAID')    
        
        await asyncio.sleep(4) 
        msg = 'Type defendNetwork(); to harness avilable blockchains and boost our firewall\'s signal.'
        await twitch_bot.say(message.channel, msg)

        await asyncio.sleep(10) 
        msg = 'Network defenses are failing. Initiate all protocols! Pizza! Donuts! Bacon!! THROW ALL WE\'VE GOT AT THEM!!'
        await twitch_bot.say(message.channel, msg)

        await asyncio.sleep(5) # 40s Pizza
        await twitch_bot.say(message.channel, "pizzaProtocol();")

                
@twitch_bot.command('raidover')
async def raidover(message):
    if is_mod(message):
        change_scene('RAID2')
        await twitch_bot.say(message.channel, "Keepo")
        await asyncio.sleep(2) #
        msg = "!disabled3"
        await twitch_bot.say(message.channel, msg)
        change_scene('GAMES')


@twitch_bot.command('bsod')
async def bsod(message):
    if is_mod(message):
        change_scene('BSOD')
   

# ─── DEBUG COMMANDS ─────────────────────────────────────────────────────────────

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


@twitch_bot.command('channel')
async def channel(message):
    await twitch_bot.say(message.channel, str(message.channel.id))


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
    

# switch scene to GAMES    
@twitch_bot.command('main')
async def main(message):
    if is_mod(message):
        change_scene('MAIN')
        msg = "Switching scene back to MAIN."
        await twitch_bot.say(message.channel, msg) 