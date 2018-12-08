from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
from playsound import playsound

# config ze bot!
twitch_bot = twitch_instance


# ─── SFX ────────────────────────────────────────────────────────────────────────

@twitch_bot.command('slideup')
async def slideup(message):
    await playsound('sfx/slideup.mp3')
