from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
import sys
import os
from permissions import is_bot, is_mod


# config ze bot!
twitch_bot = twitch_instance


###############################################################################
# SECTION Graphics & Overlay Content
###############################################################################

def display_task_on_obs(task):
    f = open('data\\task.txt', 'w+')
    f.write('!task = {}'.format(task))
    f.close()

# !SECTION 


###############################################################################
# SECTION OBS Scene Control
###############################################################################

def change_scene(scene):
    """
    **Requires 'Advance Scene Switcher' plug-in**
    Swap scenes in OBS studio by writing the scene name to a file.
    """
    f = open('data\\scene_next.txt', 'w+')
    f.write(scene)
    f.close()


def get_scene():
    """
    **Requires 'Advance Scene Switcher' plug-in**
    Read current scene from OBS studio, which is writing scene names 
    to a .txt file.
    """
    f = open('data\\scene_current.txt', 'r+')
    scene = f.readline()
    f.close()
    return scene


@twitch_bot.command('obsscene')
async def obsscene(message):
    if is_mod(message):
        scene = get_scene()
        msg = '@{}, the current scene is {}'.format(message.author.name, scene)
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('obsbsod')
async def obsbsod(message):
    if is_mod(message):
        change_scene('BSOD')


@twitch_bot.command('obsintro')
async def obsintro(message):
    if is_mod(message):
        change_scene('INTRO')


@twitch_bot.command('obsswap')
async def obsswap(message):
    if is_mod(message):
        change_scene('GAMES SWAP')


@twitch_bot.command('obsraid')
async def obsswobsraidap(message):
    if is_mod(message):
        change_scene('RAID')


@twitch_bot.command('obsraid2')
async def obsraid2(message):
    if is_mod(message):
        change_scene('RAID2')


@twitch_bot.command('obsdj')
async def obsdj(message):
    if is_mod(message):
        change_scene('DJ')


# switch scene to GAMES    
@twitch_bot.command('obsmain')
async def obsmain(message):
    if is_mod(message):
        change_scene('MAIN')
        msg = "Switching scene back to MAIN."
        await twitch_bot.say(message.channel, msg) 

# !SECTION 