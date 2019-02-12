import asyncio
import time
import random
import os

# internal modules & packages
import conf
import data_tools
import integrations.twitch.api_wrapper
from integrations.twitch.privilege import is_mod
from integrations.streamelements.api_wrapper import get_points, put_points
from sfx.sfx import play_sfx

# config ze bot!
twitch_bot = conf.twitch_instance

earworm_last_used = time.time() - 60
earworm_timeout_period = 60


###############################################################################
# SECTION Earworm Roulet™ (WIP)
###############################################################################

@twitch_bot.command('earworm')
async def earworm(message):
    '[earworm] ------> [lose]'
    global earworm_last_used

    # print(f"last earworm : {time.time() - earworm_last_used}")

    # focus-mode cooldown timer
    if time.time() - earworm_last_used < earworm_timeout_period:
        msg = f"We're in focus mode tonight, @{message.author.name}. !earworm has a 60-second cooldown."
        await twitch_bot.say(message.channel, msg)
        return

    token = data_tools.tokenize(message, 2)

    bettor = message.author.name
    bet = int()

    if len(token) > 1:
        if token[1].isnumeric():
            bet = int(token[1])
        elif token[1] == 'all':
            # get the amount of points the user has & make the bet those points
            bet = get_points(bettor)
        else:
            pass
        
    
    elif len(token) == 1 or token[1].isdigit() == False:
        msg = 'Try !earworm <bet>.'
        await twitch_bot.say(message.channel, msg)
        return


    # Czeck if BETTORRR has enough points
    if get_points(bettor) < bet or bet <= 0:
        msg = f'Is you broke or somethin, @{bettor}??? You only have {get_points(bettor)} points'
        await twitch_bot.say(message.channel, msg)
        return


    # ANCHOR They win
    # random.seed('Password')
    if random.random() >= 0.5:
        put_points(bettor, bet)
        points = get_points(bettor)
        msg = f'@{bettor}, u lucked tf out! {bet} shuriken added. You have {points} now.'
        await twitch_bot.say(message.channel, msg)
        return

    # ANCHOR They lose
    put_points(bettor, -bet)
    points = get_points(bettor)
    msg = '⚰️☠️😱⚰️☠️😱⚰️☠️😱⚰️☠️😱⚰️☠️😱⚰️☠️😱⚰️☠️😱⚰️☠️😱⚰️☠️😱'
    await twitch_bot.say(message.channel, msg)
    msg = f'rip, @{bettor}. You lost {bet} shuriken. You have {points} left. Pls dun cry.'
    await twitch_bot.say(message.channel, msg)
    

    files = []

    # create a list of mp3s in folders (excluding aliases.txt)
    for file_name in os.listdir('sfx/earworms/'):
        if not file_name.endswith('.txt'):
            files.append(file_name)

    random_mp3 = f'sfx/earworms/{random.choice(files)}'

    play_sfx(random_mp3)

    earworm_last_used = time.time()
    print(f"earworm used. timer reset")

# !SECTION 