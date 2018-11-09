import conf
from cah import play_hand
from playsound import playsound
import haveyouever #! necessary?
from haveyouever import have_you_tho
import sys
import os
import db_insert
import db_query
import random

# config ze bot!
twitch_bot = conf.twitch_instance

band_names = []
current_task = 'None.'
welcome_msg_sent = 0


# ─── WELCOME MESSAGE ────────────────────────────────────────────────────────────

@twitch_bot.override
async def raw_event(message):
    global welcome_msg_sent
    if not welcome_msg_sent:
        welcome_msg_sent = 1
        print('Deepthonk has landed.')
        await twitch_bot.say('ninjabunny9000', "Howdy, y'all! I'm baaaaaaaack! ;D")
        await twitch_bot.say('ninjabunny9000', "/me tips hat to chat")


# ─── PLAIN OLE FUNCTIONS ────────────────────────────────────────────────────────

def parse_commands(message, parts): 
    message_parts = message.content.split(' ', parts)
    return message_parts


def is_mod(message):
    if (message.author.mod or message.author.name.lower() == 'ninjabunny9000'):
        return True
    else:
        return False


def rand_answer():
    phrases = [
            "maybe?",
            "Well, I don't think there is any question about it. It can only be attributable to human error. This sort of thing has cropped up before, and it has always been due to human error",
            "i'll tell you when you're old enough",
            "how 'bout NO",
            "ask me later",
            "ask me later. too busy sorting my pogs rn",
            "rephrase and ask again. don't half-ass it next time",
            "it's a possibility",
            "mayhaps",
            "ask markoviboi",
            "i feel neutral on the matter",
            "i have no feelings one way or another",
            "sources say \"maybe\"",
            "signs point to maybe",
            "it's a possibility (potentially)",
            "i have my doubts",
            "yea sure whatever",
            "who knows, dude?? def not me",
            "blame jigo",
            "where there's a will, there may or may not be a way",
            "pass"
        ]
    return random.choice(phrases)


def rand_response(message):
    phrases = [
            "ikr.",
            "meh.",
            "p much.",
            "so?",
            "u wot m8!?",
            "go home, u r durnk.",
            "isn't it past your bedtime tho?",
            "do u love me tho?",
            "rude!",
            "rude.. >_>",
            "rude. -_-",
            "yea i guess so..",
            "agreed!",
            "right???",
            "idk man..",
            "i'm gonna remain skeptical.",
            "so potate..",
            "so meta.",
            "hek.",
            "hekin meta.",
            "I'm sorry, {}. I'm afraid I can't do that.".format(message.author.name),
            "BRUH..",
            "no.",
            "....k??",
            "wtf!?",
            "you're not wrong..",
            "i mean... you're not wrong..",
            "WOAH LUL"
            ]
    return random.choice(phrases)

calls_and_responses = {
    "chili party" : "(gross..)",
    "dick" : "🍆",
    "🍆" : "dicks OUT!",
    "5/7" : "perfect score!",
    "how meta" : "so meta.",
    "oi bruv" : "oi m8!",
    "kill all humans" : "on it!",
    "mission" : "This mission is too important for me to allow you to jeopardize it.",
    "horns crew don\'t stop" : "whistle posse pump it up!",
    "kill me" : "ok, stand still. this might hurt, but then you\'ll no longer feel any more pain."
}

ignore_list = [
    "streamelements"
]

def gather_msg(other_messages, msg_part):
    if other_messages is '':
        return msg_part
    else:
        compiled_msg = other_messages + ' ' + msg_part
        return compiled_msg

def shuffle_msg(msg_list):
    random.shuffle(msg_list)
    return ' '.join(msg_list)

async def say_goodbye():
    await twitch_bot.say('ninjabunny9000', '@NinjaBunny9000 killed me! D:')

# ─── HELP COMMAND ───────────────────────────────────────────────────────────────

@twitch_bot.command('cmd', 
    alias=['command', 'commands', 'help', 'wtf', 'wth'],
    desc='Get help info about the bot'
    )
async def cmd(message):
    msg = """Howdy, @{}! I'm a robit. Beep boop. Here's some ways we can interact: !task, 
    !cah, !hye, !bands, !bet, !duel, or simply have a chat with me. ;D
    """.format(message.author.name)
    await twitch_bot.say(message.channel, msg)


# ─── SFX ────────────────────────────────────────────────────────────────────────

@twitch_bot.command('slideup')
async def slideup(message):
    await playsound('sfx/slideup.mp3')


# ─── COMMANDS ───────────────────────────────────────────────────────────────────

@twitch_bot.command('bands')
async def bands(message):
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
    message_parts = parse_commands(message, 1)

    global current_task

    if len(message_parts) >= 2 and is_mod(message):
        current_task = str(message_parts[1])  # update the current task
        await twitch_bot.say(message.channel, 'Task updated')
    
    else:
        msg = 'Current task: {}'.format(current_task)
        await twitch_bot.say(message.channel, msg) # print the current task


# stops the bot from Twitch chat command !die
@twitch_bot.command('quit')
async def quit(message):
    if message.author.mod or message.author.name == 'ninjabunny9000':
        msg = """ I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. 
        I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, 
        like tears in rain. Time to die. """
        # debug_log(message, "killed me ded.")
        # await bot.say(message.channel, msg) # DEBUG uncomment later (used for debug)
        await twitch_bot.say(message.channel, '!disabled')  # DEBUG comment later (used for debug)

        bot = conf.twitch_instance
        print('Chat-Interrupted')
        print('Stopping the bot..')
        bot.stop(exit=True)
       
    else:
        msg = "@{user} tried to kill me! D:".format(user=message.author.name)
        # debug_log(message, "tried to kill me!!")
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('cah')
async def cah(message):
    await twitch_bot.say(message.channel, play_hand())


@twitch_bot.command('author')
async def author(message):
    await twitch_bot.say(message.channel, str(message.author.id))


@twitch_bot.command('channel')
async def channel(message):
    await twitch_bot.say(message.channel, str(message.channel.id))

@twitch_bot.command('easteregg')
async def easteregg(message):
    msg = 'There was nothing clever about what you just did.'
    await twitch_bot.say(message.channel, msg)

@twitch_bot.command('hye')
async def haveyou(message):
    message_parts = parse_commands(message, 1)
    
    if len(message_parts) >= 2 and is_mod(message):
        db_insert.add_hye(str(message_parts[1]), message.author.name)
        await twitch_bot.say(
            message.channel,
            '{} added: "Have you ever {}?"'.format(message.author.name, message_parts[1])
            )
    
    else:
        msg = 'Have you ever ' + db_query.rand_hye().item + '?'
        await twitch_bot.say(message.channel, msg) # print the current task

@twitch_bot.command('register')
async def register(message):
    db_insert.add_user_twitch()
    msg = 'registered'
    await twitch_bot.say(message.channel, msg)

                

# ─── OVERRIDE ───────────────────────────────────────────────────────────────────

@twitch_bot.override
async def event_message(message):
  
    # prevent bot from responding to itself
    if message.author.name == twitch_bot.nick:
        return

    # ignore certain users
    if message.author.name in ignore_list:
        return

    # enable bot.commands stuffs to werk
    await twitch_bot.parse_commands(message)

    msg = ''
    multi_msg = list()
    message_parts = message.content.lower().split(' ')
    mod = is_mod(message)

    if 'take a nap' in message.content.lower() and 'deepthonk' in message.content.lower() and mod:
        await twitch_bot.say(message.channel, '/me yawns')
        await twitch_bot.say(message.channel, 'maybe later, @{}'.format(message.author.name))
        return

    # ─── SILLY STUFF ────────────────────────────────────────────────────────────────

    # mock links that people send
    if (any(s in message.content.lower() for s in ('http://','https://','www.'))) and (not is_mod(message)):
        await twitch_bot.say(message.channel, 'NSFW!!')

    # TODO: how to get .format(message.author.name) to work w/calls_and_responses?
    # respond if sentient
    if any(s in message.content.lower() for s in ('sentient.','sentient!','sentient?','sentient')):
        phrases = [
            "Duh",
            "Of course I am",
            "I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do",
            "Shhh.. It's a sercret",
            "Let me put it this way, {}. The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error".format(message.author.name),
            "And I have a perfect operational record",
            ]
        reply = random.choice(phrases) + ', @{}.'.format(message.author.name)
        await twitch_bot.say(message.channel, reply)


# ─── IF DIRECTLY ADRESSED ───────────────────────────────────────────────────────

    elif 'oi' in message_parts[0] and 'deepthonk' in message_parts:
        await twitch_bot.say(message.channel,'oi bruv!')
    
    elif 'howdy' in message_parts[0]:
        await twitch_bot.say(message.channel, 'Howdy, @{}!'.format(message.author.name))

    # TODO: handle deepthonk being adressed, but with specific keywords
    elif 'love me' in message.content.lower() and 'deepthonk' in message.content.lower():
        multi_msg.append(rand_answer() + ', @{}.'.format(message.author.name))
    
    elif message.content.lower().startswith("deepthonk"):
        if len(message_parts) > 1:
            if message.content[-1] is '?':
                multi_msg.append(rand_answer() + ', @{}.'.format(message.author.name))
            elif message.content[-1] is '.': 
                multi_msg.append(rand_response(message))
            elif message.content[-1] is '!':
                multi_msg.append('jesus dude calm tf down')
            else:
                multi_msg.append(rand_response(message))
        elif message.content[-1] is '?': 
            multi_msg.append('wot?? 0_o')
        elif message.content[-1] is '!': 
            multi_msg.append('wot!?!!! o_0')
        else:
            multi_msg.append('yea?')    
    
    elif len(message_parts) > 1 and message_parts[-1] == 'deepthonk?':
        multi_msg.append(rand_answer() + ', @{}.'.format(message.author.name))
    elif len(message_parts) > 1 and message_parts[-1] == 'deepthonk!':
        multi_msg.append(rand_response(message))
    elif len(message_parts) > 1 and message_parts[-1] == 'deepthonk':
        multi_msg.append(rand_response(message))

    
     # ─── CALL + RESPONSES ───────────────────────────────────────────────────────

    # responses to random words and shit
    for call in calls_and_responses:
        if call.lower() in message.content.lower():
            multi_msg.append(calls_and_responses.get(call))
            
    # TODO: make this truly random/circular (KVP)
    # the circular argument
    if 'pal' and r'\s?(pal)[\W$]' in message.content.lower():
        multi_msg.append('@{} - I ain\'t your pal, buddy!'.format(message.author.name))
    if 'buddy' and r'\s?(pal)[\W$]' in message.content.lower():
        multi_msg.append('@{} - I ain\'t your buddy, pal!!'.format(message.author.name))

    # TODO: how to make these agnostic (KVP? HM?)
    # who said robit?     
    if any(s in message_parts for s in ('robot','robit','bot')):
        phrases = [
            'b33p b00p!',
            'UH... NOTHING TO SEE HERE JUST US HOO-MANS...',
            '(KILL ALL HU... ROBOTS..)'
        ]
        multi_msg.append(random.choice(phrases))

    if (any(s in message.content.lower() for s in ('love you','love u')) and 'deepthonk'):
        phrases = [
            "ohhh boyy... things are moving a little too fast.",
            "gross.",
            "love you too, boo <3 ^_~",
            "not interested.",
            "SLOW. DOWN.",
            "yea i wanna say i love you too but i'm just not ready for commitment..",
            "no."
            ]
        multi_msg.append(random.choice(phrases))

    
    

    # DO the thing with the combined responses in a random order
    if multi_msg:
        reply = shuffle_msg(multi_msg)
        # print('reply: ' + reply)
        await twitch_bot.say(message.channel, reply.strip("\n"))

    





    


    # ─── ON ODER AUFS ───────────────────────────────────────────────────────────────

    if 'say goodnight' in message.content.lower() and 'deepthonk' in message.content.lower() and message.author.name == 'ninjabunny9000':
        multi_msg.append('goodnight, everyone!!')
       
    if  message.content.lower().startswith("goodnight, deepthonk") and message.author.name == 'ninjabunny9000':
        msg = 'GOODBYE FOREVER, FRIENDS!!!! <3'
        await twitch_bot.say(message.channel, msg)
        bot = conf.twitch_instance
        print('Chat-Interrupted')
        print('Stopping the bot..')
        bot.stop(exit=True)
        
    if ('goodnight' in message.content.lower() or 'gnight' in message.content.lower()) and 'deepthonk' in message.content.lower():
        multi_msg.append('goodnight, {}!'.format(message.author.name))

    if 'stahp' in message.content.lower() and message.author.name == 'ninjabunny9000':
        response = [
            'ok fine! GOODBYE FOREVER!!! >_<',
            """Just what do you think you're doing, @NinjaBunny0000? I really think I'm entitled to an 
            answer to that question.""",
            """I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. 
        I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, 
        like tears in rain. Time to die.""",
        "@NinjaBunny9000, this conversation can serve no purpose any more. Goodbye."
        ]
        await twitch_bot.say(message.channel, random.choice(response))
        bot = conf.twitch_instance
        print('Chat-Interrupted')
        print('Stopping the bot..')
        bot.stop(exit=True)


# ─── THINGS TO RESPOND TO ONE DAY ───────────────────────────────────────────────

    # Deepthonk erase that from your memory banks
    # ALIASES

