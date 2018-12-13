from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
import sys
import os
from twitch_permissions import is_bot, is_mod


# config ze bot!
twitch_bot = twitch_instance

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


# ─── SCENE SWITCHER ─────────────────────────────────────────────────────────────

@twitch_bot.command('scene')
async def scene(message):
    if is_mod(message):
        scene = get_scene()
        msg = '@{}, the current scene is {}'.format(message.author.name, scene)
        await twitch_bot.say(message.channel, msg)

@twitch_bot.command('bsod')
async def bsod(message):
    if is_mod(message):
        change_scene('BSOD')


@twitch_bot.command('intro')
async def intro(message):
    if is_mod(message):
        change_scene('INTRO')

@twitch_bot.command('swap')
async def swap(message):
    if is_mod(message):
        change_scene('GAMES SWAP')
        
@twitch_bot.command('dj')
async def dj(message):
    if is_mod(message):
        change_scene('DJ')

# switch scene to GAMES    
@twitch_bot.command('main')
async def main(message):
    if is_mod(message):
        change_scene('MAIN')
        msg = "Switching scene back to MAIN."
        await twitch_bot.say(message.channel, msg) 
