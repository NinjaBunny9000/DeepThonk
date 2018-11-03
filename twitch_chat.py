import conf
import cah
from cah import play_hand
from playsound import playsound
import haveyouever
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

# @twitch_bot.override
# async def event_ready(message):
#     twitch_bot.say('ninjabunny9000', 'Hello, y\'all!')

print('Twitch bot imported...')

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
            "maybe? ¯\_(ツ)_/¯",
            "ask again later, ya chump.",
            "better not tell you now..",
            "i'll tell you when you're old enough",
            "i'll tell you later",
            "ask me later",
            "cannot predict now. busy sorting my pogs.",
            "rephrase and ask again. don't half-ass it next time.",
            "well...i woudn't count on it - but you might!",
            "it's a possibility.",
            "it is decidedly unknown.",
            "mayhaps",
            "i feel neutral on the matter",
            "i have no feelings one way or another",
            "my reply is.. mayhaps.",
            "sources say maybe!",
            "outlook decidedly \"OK\".",
            "outlook... not so OK.",
            "reply hazy, try again.",
            "signs point to maybe. (maybe)",
            "it's a possibility, potentially.",
            "i have my doubts, but then again..",
            "yea sure whatever.",
            "nah fam.",
            "yea.. no...maybe!?? ..what was teh question again?",
            "who knows, dude?? who knows...",
            "blame jigo"
        ]
    return random.choice(phrases)

def rand_response():
    phrases = [
            "ikr",
            "meh",
            "p much",
            "so?",
            "u wot m8!?",
            "go home, u r durnk.",
            "isn't it past your bedtime tho",
            "do u love me tho?",
            "rude!",
            "rude.. >_>",
            "rude. -_-",
            "yea i guess so",
            "agreed",
            "right???",
            "idk man..",
            "i'm gonna remain skeptical",
            "so potate..",
            "so meta",
            "hek",
            "hekin meta",
            "BRUH..",
            "no.",
            "....k",
            "wtf!?"
            ]
    return random.choice(phrases)


@twitch_bot.command('slideup')
async def slideup(message):
    await playsound('sfx/slideup.mp3')


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
    # msg = cah.play_hand()
    await twitch_bot.say(message.channel, play_hand())


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
        

# @twitch_bot.raw_event
# async def event_private_message(message):
#     print('pm recv\'d')
#     await twitch_bot.say('ninjabunny9000', 'pm recv\'d')


@twitch_bot.override
async def event_message(message):
    # your handling here
    await twitch_bot.parse_commands(message)

    # prevent bot from responding to itself
    if message.author.name == twitch_bot.nick:
        return

    # you should feel bad for this
    if message.content.lower().startswith("!easteregg"):
        msg = "There was nothing clever about what you just did."
        # debug_log(message, str(msg))
        await twitch_bot.say(message.channel, msg)


    # ─── ON ODER AUFS ───────────────────────────────────────────────────────────────

    if 'say goodnight' in message.content.lower() and 'deepthonk' in message.content.lower() and message.author.name == 'ninjabunny9000':
        msg = 'goodnight, everyone!!'
        await twitch_bot.say(message.channel, msg)

    if  message.content.lower().startswith("goodnight, deepthonk") and message.author.name == 'ninjabunny9000':
        msg = 'GOODBYE FOREVER, FRIENDS!!!! <3'
        await twitch_bot.say(message.channel, msg)
        bot = conf.twitch_instance
        print('Chat-Interrupted')
        print('Stopping the bot..')
        bot.stop(exit=True)
        
    if ('goodnight' in message.content.lower() or 'gnight' in message.content.lower()) and 'deepthonk' in message.content.lower():
        msg = 'goodnight, {}!'.format(message.author.name)
        await twitch_bot.say(message.channel, msg)


    # ─── DIRECT COMS ────────────────────────────────────────────────────────────────
        
    if message.content.lower().startswith("deepthonk"):
        message_parts = message.content.split(' ')
        if len(message_parts) > 1:
            if message.content[-1] is '?':
                await twitch_bot.say(message.channel, rand_answer())
            elif message.content[-1] is '.': 
                await twitch_bot.say(message.channel, rand_response())
            elif message.content[-1] is '!':
                await twitch_bot.say(message.channel, 'jesus dude calm tf down')
            else:
                await twitch_bot.say(message.channel, rand_response())
        elif message.content[-1] is '?': 
            await twitch_bot.say(message.channel, 'wot?? 0_o')
        elif message.content[-1] is '!': 
            await twitch_bot.say(message.channel, 'wot!?!!! o_0')

    message_parts = message.content.split(' ')
    if len(message_parts) > 1 and message_parts[-1] == 'deepthonk?':
        await twitch_bot.say(message.channel, rand_answer())
    elif len(message_parts) > 1 and message_parts[-1] == 'deepthonk!':
        await twitch_bot.say(message.channel, rand_response())
    elif len(message_parts) > 1 and message_parts[-1] == 'deepthonk':
        await twitch_bot.say(message.channel, rand_response())

    
     # ─── CALL + RESPONSES ───────────────────────────────────────────────────────

    # responses to random words and shit
    if 'pal' in message.content.lower():
        msg = "@{} - I ain't your pal, buddy!".format(message.author.name)
        await twitch_bot.say(message.channel, msg)

    if 'buddy' in message.content.lower():
        msg = "@{} - I ain't your buddy, pal!!".format(message.author.name)
        await twitch_bot.say(message.channel, msg)

    if 'chili party' in message.content.lower():
        msg = "gross.."
        await twitch_bot.say(message.channel, msg)

    if 'dick' in message.content.lower():
        msg = "🍆"
        await twitch_bot.say(message.channel, msg)

    if '🍆' in message.content.lower():
        msg = "dicks OUT!"
        await twitch_bot.say(message.channel, msg)
        
    if 'howdy' in message.content.lower():
        msg = 'Howdy, @{}!'.format(message.author.name)
        await twitch_bot.say(message.channel, msg)

    if '5/7' in message.content.lower():
        msg = 'perfect score!'
        await twitch_bot.say(message.channel, msg)

    if 'kill me' in message.content.lower():
        msg = 'ok, stand still. this might hurt, but then you\'ll no longer feel any more pain.'
        await twitch_bot.say(message.channel, msg)

    if 'robot'in message.content.lower() or 'robit' in message.content.lower() or 'bot' in message.content.lower():
        msg = 'beep boop'
        await twitch_bot.say(message.channel, msg)

    if 'http://' in message.content.lower() or 'https://' in message.content.lower() or 'www.' in message.content.lower():
        msg = 'NSFW!!'
        await twitch_bot.say(message.channel, msg)

    if 'stahp' in message.content.lower() and message.author.name == 'ninjabunny9000':
        msg = 'ok fine! GOODBYE FOREVER!!! >_<'
        await twitch_bot.say(message.channel, msg)
        bot = conf.twitch_instance
        print('Chat-Interrupted')
        print('Stopping the bot..')
        bot.stop(exit=True)
    
    if ('sentient.' or 'sentient!') in message.content.lower():
        msg = 'Duh, {}.'.format(message.author.name)
        await twitch_bot.say(message.channel, msg)
    elif 'sentient?' in message.content.lower():
        msg = 'Of course I am, {}.'.format(message.author.name)
        await twitch_bot.say(message.channel, msg)
    elif 'sentient' in message.content.lower():
        msg = 'Of course I am, {}.'.format(message.author.name)
        await twitch_bot.say(message.channel, msg)

    if 'horns crew' in message.content.lower():
        msg = "whistle posse!"
        await twitch_bot.say(message.channel, msg)
    elif 'horns crew don\'t stop' in message.content.lower():
        msg = "whistle posse pump it up!"
        await twitch_bot.say(message.channel, msg)

    if ('love you' in message.content.lower() or 'love u' in message.content.lower()) and 'deepthonk' in message.content.lower() :
        phrases = [
            "ohhh boyy... things are moving a little too fast",
            "gross",
            "love you too, boo <3 ^_~",
            "not interested",
            "SLOW. DOWN.",
            "yea i wanna say i love you too but i'm just not ready for commitment",
            "no."
            ]
        msg = random.choice(phrases)
        await twitch_bot.say(message.channel, msg)

    if 'love me' in message.content.lower() and 'deepthonk' in message.content.lower():
        await twitch_bot.say(message.channel, rand_answer)
    
    

