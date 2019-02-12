import random
import sys
import os
import asyncio

# internal modules & packages
import conf
import content
from integrations.obs.ctrl import change_scene
from integrations.twitch.privilege import is_bot, is_mod
import games.raid
import data_tools
from sfx.sfx import play_sfx

# config ze bot!
twitch_bot = conf.twitch_instance
welcome_msg_sent = 0


###############################################################################
# SECTION Raw Events
###############################################################################

@twitch_bot.override
async def raw_event(message):
    global welcome_msg_sent
    if not welcome_msg_sent:
        welcome_msg_sent = 1
        welcome_msg = conf.bot_settings['welcome_msg']
        print(conf.bot_name.capitalize() + ' has landed.')
        await twitch_bot.say(conf.twitch_channel, welcome_msg)
        play_sfx('sfx/hooks/back.mp3')
        await twitch_bot.say(conf.twitch_channel, "/me tips fedora to chat")

        # make initial list of people in the room
        games.raid.update_defenders_list()


@twitch_bot.override
async def event_user_join(user):
    # if raid is happening
    if games.raid.start():
        pass
    else:
        games.raid.append_defenders(user.name)


@twitch_bot.override
async def event_user_leave(user):
    pass

# !SECTION 





###############################################################################
# SECTION event_message
###############################################################################

@twitch_bot.override
async def event_message(message):
    """
    Each message in chat is sent through this command.
    
    Parse teh data (into tokens, ofc), add a conditional or two, and make all
    sorts of fun stuff happen!
    """
    # enable bot.commands stuffs to werk
    await twitch_bot.parse_commands(message)

    # prevent bot from responding to itself unless it's emotes in a message
    if not games.raid.is_happening() and not message.emotes:
        if message.author.name == twitch_bot.nick:
            return

    # ignore blacklisted users
    for user in conf.ignore_list:
        if message.author.name.lower() == user.lower():
            return

    multi_msg = list()  # creates an empty list for messages to get shuffled and responded with
    message_parts = data_tools.tokenize(message)  # TOKENIZE™
    mod = is_mod(message)
    bot = conf.bot_name.lower()

    # return FAQ's
    if content.faq(message):
        msg = content.faq(message)
        await twitch_bot.say(message.channel, msg)


    ###########################################################################
    # ANCHOR Raid Stuffs
    ###########################################################################

    if games.raid.is_happening():

        # append emote-sending members to the correct list
        games.raid.append_raiders(message)

        # count & score emotes
        if message.emotes:   

            games.raid.deal_damage(message)

            # TODO logging
            print(f'defending.hp= {games.raid.defending.hp} || raiding.hp={games.raid.raiding.hp}')

            # prints hp to .txt file
            data_tools.score_to_txt(games.raid.defending.hp, games.raid.raiding.hp)

            # WIN CONDITION EVENTS
            if games.raid.report_ko():

                games.raid.stop()
                raid_winner = games.raid.get_winner() 
                
                play_sfx('sfx/events/raid_victory.mp3')

                # report the victor
                raid_over_msg = conf.raid['raid_over']
                msg = f'{raid_over_msg} The victor is {raid_winner}!'
                await twitch_bot.say(message.channel, msg)

                if conf.raid['custom_victory_scene']:
                    asyncio.sleep(conf.raid['victory_timer'])
                    change_scene(conf.raid['victory_scene'])
    else:
        # add people to defenders list
        games.raid.append_defenders(message.author.name)
                    


    ###########################################################################
    # ANCHOR Link-handling (_It's dangerous to go alone.._)
    ###########################################################################

    # mock links that people send
    if any(s in message.content.lower() for s in ('http://','https://','www.')) and not mod:
        await twitch_bot.say(message.channel, conf.bot_settings['link_msg'])

    # respond if sentient
    if any(s in message.content.lower() for s in ('sentient.','sentient!','sentient?','sentient')):
        await twitch_bot.say(message.channel, content.sentient(message))


    ###########################################################################
    # ANCHOR Addressing (talking to) the bot
    ###########################################################################

    # REVIEW This is a mess, and I hate it.

    # cuz your bot is from Texas
    elif 'howdy' in message_parts[0]:
        await twitch_bot.say(message.channel, f'Howdy, @{message.author.name}!')

    # REVIEW Convert to dictionary/key-function refs
    # handles when the bot is mentioned/adressed in a message, or asked a question
    elif message.content.lower().startswith(bot):
        if len(message_parts) > 1:
            if message.content[-1] is '?':
                multi_msg.append(content.binary_responses() + f', @{message.author.name}.')
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
        multi_msg.append(content.binary_responses() + f', @{message.author.name}.')
    elif len(message_parts) > 1 and message_parts[-1] == bot + '!':
        multi_msg.append(content.generic_responses(message))
    elif len(message_parts) > 1 and message_parts[-1] == bot:
        multi_msg.append(content.generic_responses(message))

    
    ###########################################################################
    # ANCHOR Calls & Responses
    ###########################################################################
            
    # responses to random words in messages. customize in content.py
    msg = content.get_response_to_call(message)
    if msg is not None:
        multi_msg.append(msg)

    # who said robit?     
    if any(s in message_parts for s in ('robot','robit','bot')):
        multi_msg.append(content.someone_sed_robit())

    # for use by Robosexuals™ only!
    if (any(s in message.content.lower() for s in ('love you','love u', 'love me')) and bot):
        play_sfx('sfx/hooks/norobo.mp3')
        multi_msg.append(content.love_or_nah())

    # Combine all responses in a random order and send them in chat
    if multi_msg:
        reply = data_tools.shuffle_msg(multi_msg)
        # print('reply: ' + reply)
        await twitch_bot.say(message.channel, reply.strip("\n"))

    # sum1 sed fortnite
    if 'play' in message.content.lower() and 'fortnite' in message.content.lower():
        msg = 'y would u even think that, @{message.author.name}??'
        await twitch_bot.say(message.channel, msg)
        await twitch_bot.say(message.channel,f'/timeout {message.author.name} 30')

    elif 'fortnite' in message.content.lower():
        msg = 'who sed fortnite!?!!??...'
        await twitch_bot.say(message.channel, msg)
        await twitch_bot.say(message.channel,f'/timeout {message.author.name} 15')


###############################################################################
# SECTION Bot On / Off Control
###############################################################################

# make it stahp
off_cmd = conf.bot_settings['off_cmd'].lower()
@twitch_bot.command(off_cmd)
async def off(message):
    if message.author.mod or message.author.name == conf.streamer:
        play_sfx('sfx/hooks/oof.mp3')
        await twitch_bot.say(message.channel, content.last_words())  # DEBUG comment later (used for debug)
        bot = conf.twitch_instance
        print('Chat-Interrupted')
        print('Stopping the bot..')
        bot.stop(exit=True)
       
    else:
        msg = f"@{message.author.name} tried to kill me! D:"
        print(msg)
        await twitch_bot.say(message.channel, msg)

    # !SECTION 

# !SECTION 


###############################################################################
# SECTION "What do?" (where does this stuff go???)
###############################################################################

@twitch_bot.command('so')
async def so(message):
    if is_mod(message):
        token = data_tools.tokenize(message, 2)
        streamer = data_tools.ats_or_nah(token[1])
        try:
            msg = f"Big ups to @{streamer}! They're a friend of the stream and \
            worth a follow, if you have the time! https://twitch.tv/{streamer}"
            await twitch_bot.say(message.channel, msg)
        except:
            msg = f"You didn't include a streamer to shout out to, {message.author.name}."
            await twitch_bot.say(message.channel, msg)

# !SECTION 


###############################################################################
# SECTION Debug Tools
###############################################################################

# REVIEW Purge these during the next refactor 

# !SECTION 


###############################################################################
# SECTION Easter Eggs
###############################################################################

@twitch_bot.command('easteregg')
async def easteregg(message):
    """
    Just an easter egg.
    """
    await twitch_bot.say(message.channel, content.easter_egg(message))

# !SECTION 