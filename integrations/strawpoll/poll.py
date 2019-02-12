import sys
import os


# internal modules & packages
import conf
from integrations.twitch.privilege import is_mod
import data_tools
from sfx.sfx import play_sfx

from .api_wrapper import add_option, set_name, setup_poll, review_poll, get_link, get_winner


# config ze bot!
twitch_bot = conf.twitch_instance

"""
#################### PROTOTYPE EXAMPLE ########################
!poll add <poll title goes here>
deepthonk: @<mod> Poll initiated. Awaiting options...
!poll opt <option 1 goes here>
!poll opt <option 2 goes here>
!poll opt <option 3 goes here>
!poll review
deepthonk: <poll preview>
!poll <accept/cancel>
deepthonk: Here's a link to the poll: <url>
###############################################################
"""

# hacky (at best)
def reset_poll():
    global poll_url
    global poll_name
    global poll_options

    poll_url = ''
    poll_name = ''
    poll_options = []


# FUCK FUCK FUCK FUCK WHY DID I DO THIS FUCK FUCK FUCK
@twitch_bot.command('poll')
async def poll(message):
    """ it's ok it works fine now """

    # establish/declare variables we'll be using in this function
    user = message.author.name
    global poll_url
    global poll_name
    global poll_options

    token = data_tools.tokenize(message, 2, lower_case=False) # TOKENIZE™

    'ex: !poll add What round will Bun die in?'

    # listyboi = ['!poll', 'add', 'What round will Bun die in?']

    # listyboi[2]

    # check if they're a mod
    if not is_mod(message) or len(token) == 1:
        # drop a link to the current poll if they aren't
        msg = f"@{user}, you can find the poll at {get_link()}"
        await twitch_bot.say(message.channel, msg)
        return

    # handle adding the title of the poll
    if token[1] == 'add':
        # set the name of the title (token[2])
        set_name(token[2])

    # add options to the poll
    elif token[1] == 'opt':
        # append option to list
        add_option(token[2])

    # review the poll (if needed)
    elif token[1] == 'review':
        # a way to review the poll (if needed) - mostly for debug porpuses
        poll = review_poll()
        await twitch_bot.say(message.channel, poll)

    # send the linkypost for the poll
    elif token[1] == 'accept':
        await twitch_bot.say(message.channel, setup_poll())
        # send the data to the api thingy
        # get the data back & report link in a message

    # cancel the poll
    elif token[1] == 'cancel':
        reset_poll()
        # reset all teh poll vars

@twitch_bot.command('endpoll')
async def endpoll(message):
    msg = f"The poll is over! The winning something something is {get_winner()}"
    await twitch_bot.say(message.channel, msg)