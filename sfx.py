from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
from playsound import playsound
import os, random


# config ze bot!
twitch_bot = twitch_instance


# ─── SFX ────────────────────────────────────────────────────────────────────────

@twitch_bot.command('slideup')
async def slideup(message):
    await playsound('sfx/slideup.mp3')


@twitch_bot.command('wow')
async def wow(message):
    random_mp3 = 'sfx/wow/' + random.choice(os.listdir('D:/Repos/actaulBunBot9000/sfx/wow/'))
    await playsound(random_mp3)


@twitch_bot.command('futurama')
async def futurama(message):
    random_mp3 = 'sfx/futurama/' + random.choice(os.listdir('D:/Repos/actaulBunBot9000/sfx/futurama/'))
    await playsound(random_mp3)
