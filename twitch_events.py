import conf
from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
from cah import play_hand
import sys
import os
import db_insert
import db_query
import random
import content
import asyncio
import re
from privilege import is_bot, is_mod
# REVIEW Get rid of the from games import __
import games
from games import raid_in_progress, deal_damage
import data_tools
from sfx import play_sfx


# config ze bot!
twitch_bot = twitch_instance
welcome_msg_sent = 0

# load bot settings from yaml config file to dict
custom_settings = conf.get_custom_settings()


###############################################################################
# SECTION Raw Events
###############################################################################

@twitch_bot.override
async def raw_event(message):
    global welcome_msg_sent
    if not welcome_msg_sent:
        welcome_msg_sent = 1
        welcome_msg = custom_settings['welcome_msg']
        print(conf.bot_name().capitalize() + ' has landed.')
        await twitch_bot.say(twitch_channel(), welcome_msg)
        await twitch_bot.say(twitch_channel(), "/me tips fedora to chat")

        # make initial list of people in the room
        games.update_defenders_list()


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

# !SECTION


###############################################################################
# SECTION Help Commands
###############################################################################

help_commands = conf.get_custom_settings()
help_commands = help_commands["help_cmds"]


@twitch_bot.command('help', alias=help_commands)
async def cmd(message):
    play_sfx('sfx/hooks/murderbot.mp3')
    await twitch_bot.say(message.channel, content.help_menu(message))

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

    # prevent bot from responding to itself unless it's emotes in a message
    if not games.raid_is_happening() and not message.emotes:
        if message.author.name == twitch_bot.nick:
            return

    # ignore blacklisted users
    for user in conf.ignore_list:
        if message.author.name.lower() == user.lower():
            return

    # enable bot.commands stuffs to werk
    await twitch_bot.parse_commands(message)

    multi_msg = list()  # creates an empty list for messages to get shuffled and responded with
    message_parts = data_tools.tokenize(message)  # TOKENIZE™
    mod = is_mod(message)
    bot = conf.bot_name().lower()

    # return FAQ's
    if content.faq(message):
        msg = content.faq(message)
        await twitch_bot.say(message.channel, msg)

    ###########################################################################
    # ANCHOR Raid Stuffs
    ###########################################################################

    if games.raid_is_happening():

        # count & score emotes
        if message.emotes:

            deal_damage(message)

            # TODO logging
            print(
                f'raiding.hp={games.raiding.hp} || defending.hp={games.defending.hp}')

            # prints hp to .txt file
            data_tools.score_to_txt(games.defending.hp, games.raiding.hp)

            # WIN CONDITION EVENTS
            if games.report_ko():

                games.end_raid()
                raid_winner = games.get_winner()

                play_sfx('sfx/events/raid_victory.mp3')
                # TODO Switch scenes to "victory" scene?

                # report the victor
                msg = f'{custom_settings["raid_over"]} The victor is {raid_winner}!'
                await twitch_bot.say(message.channel, msg)

    ###########################################################################
    # ANCHOR Link-handling (_It's dangerous to go alone.._)
    ###########################################################################

    # mock links that people send
    if re.search(r'(http(s)?://|www.)', message.content, re.IGNORECASE) and not mod:
        await twitch_bot.say(message.channel, custom_settings['link_msg'])

    # respond if sentient
    if re.search(r'\bsentient', message.content, re.IGNORECASE):
        await twitch_bot.say(message.channel, content.sentient(message))

    ###########################################################################
    # ANCHOR Addressing (talking to) the bot
    ###########################################################################

    # REVIEW This is a mess, and I hate it.

    # cuz your bot is from Texas
    elif re.search(r'\bhowdy\b', message_parts[0], re.IGNORECASE):
        await twitch_bot.say(message.channel, f'Howdy, @{message.author.name}!')

    # REVIEW Convert to dictionary/key-function refs
    # handles when the bot is mentioned/adressed in a message, or asked a question
    elif message.content.lower().startswith(bot):
        if len(message_parts) > 1:
            if message.content[-1] is '?':
                multi_msg.append(content.binary_responses() +
                                 f', @{message.author.name}.')
            elif message.content[-1] is '.':
                multi_msg.append(content.generic_responses(message))
            elif message.content[-1] is '!':
                multi_msg.append(content.stop_yelling_at_me())  # pls do not D:
            else:
                multi_msg.append(content.generic_responses(message))
        elif message.content[-1] is '?':
            multi_msg.append('wot?? 0_o')
        elif message.content[-1] is '!':
            multi_msg.append('wot!?!!! o_0')
        else:
            multi_msg.append('yea?')

    elif len(message_parts) > 1 and message_parts[-1] == bot + '?':
        multi_msg.append(content.binary_responses() +
                         f', @{message.author.name}.')
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
    if re.search(r'(robot|robit|bot)', message.content, re.IGNORECASE):
        multi_msg.append(content.someone_sed_robit())

    # for use by Robosexuals™ only!
    if re.search(r'love (you|u|me)', message.content, re.IGNORECASE) and bot:
        play_sfx('sfx/hooks/norobo.mp3')
        multi_msg.append(content.love_or_nah())

    # Combine all responses in a random order and send them in chat
    if multi_msg:
        reply = data_tools.shuffle_msg(multi_msg)
        # print('reply: ' + reply)
        await twitch_bot.say(message.channel, reply.strip("\n"))

    # sum1 sed fortnite
    # Matches with message content that contains the words 'fortnite' and 'play' in any order
    if re.search(r'^(?=.*\bfortnite.*\b)(?=.*\bplay.*\b).*$', message.content, re.IGNORECASE):
        msg = 'y would u even think that, @{message.author.name}??'
        await twitch_bot.say(message.channel, msg)
        await twitch_bot.say(message.channel, f'/timeout {message.author.name} 30')

    elif re.search(r'\bfortnite\b', message.content, re.IGNORECASE):
        msg = 'who sed fortnite!?!!??...'
        await twitch_bot.say(message.channel, msg)
        await twitch_bot.say(message.channel, f'/timeout {message.author.name} 15')


###############################################################################
# SECTION Bot On / Off Control
###############################################################################

# make it stahp
off_cmd = custom_settings['off_cmd'].lower()


@twitch_bot.command(off_cmd)
async def off(message):
    if message.author.mod or message.author.name == conf.streamer:
        # DEBUG comment later (used for debug)
        await twitch_bot.say(message.channel, content.last_words())
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

@twitch_bot.command('shoutout')
async def shoutout(message):
    if is_mod(message):
        msg_parts = data_tools.tokenize(message, 2)
        try:
            msg = f"Big ups to @{msg_parts[1]}! They're a friend of the stream and worth a follow, if you have the time! https://twitch.tv/{msg_parts[1]}"
        except:
            msg = f"You didn't include a streamer to shout out to, {message.author.name}."
            await twitch_bot.say(message.channel, msg)

# !SECTION


###############################################################################
# SECTION Debug Tools
###############################################################################

# REVIEW Purge these during the next refactor

@twitch_bot.command('debug')
async def debug(message):
    """
    DEBUG: change msg var to print whatever var u tryin'a lern gooder
    """
    msg = conf.debug_yaml()
    await twitch_bot.say(message.channel, msg)

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
