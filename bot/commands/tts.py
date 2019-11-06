from config.importer import bot, data
from server_interface import emit_tts
from utils.logger import loggymclogger as log

log.debug(f"{__name__} loaded")

# TODO: better permissions system
@bot.command(name='tts')
async def tts(ctx):
    'Lets chat use TTS w/o cheers or other events.'

    if ctx.author.is_mod:
        ctx.author.subscriber = 1

    if 'founder' in ctx.author.badges.keys():
        ctx.author.subscriber = 1

    # check if tts is on or nah
    if data.get_setting('tts') is False:
        await ctx.send(f"@{ctx.author.name} => TTS is temporarily disabled.")
        return

    # boot non-subbers out if in tts sub-only mode
    if data.get_setting('sub_only') is True and ctx.author.subscriber == 0:
        await ctx.send(f"@{ctx.author.name} TTS is for subscribers only right now.")
        return

    # do the tts thing
    print(ctx.content)
    token = ctx.content.split(' ',1)
    await emit_tts(token[1])
    log.debug(f'tts request detected in chat: {token[1]}')


@bot.command(name='ttson')
async def ttson(ctx):
    if ctx.author.is_mod is False:
        return
    if data.get_setting('tts') is False:
        data.set_setting('tts', True)
        await ctx.send(f"TTS turned back on..")
    else:
        await ctx.send(f"TTS is already on.")


@bot.command(name='ttsoff')
async def ttsoff(ctx):
    if ctx.author.is_mod is False:
        return
    if data.get_setting('tts') is True:
        data.set_setting('tts', False)
        await ctx.send(f"TTS temporarily disabled.")
    else:
        await ctx.send(f"TTS is already off.")


@bot.command(name='ttssub')
async def ttssub(ctx):
    'Toggle TTS being sub-only or nah'
    if ctx.author.is_mod is False:
        return
    msg = f"TTS is now "
    if data.get_setting('sub_only') is False:
        msg += "in sub-only mode."
        data.set_setting('sub_only', True)
    else:
        msg += "free for everyone to use (responsibly)."
        data.set_setting('sub_only', False)
    await ctx.send(msg)


@bot.command(name='ttsmode')
async def ttsmode(ctx):
    'Reports who can use TTS in chat.'
    msg = 'TTS are '
    if data.get_setting('sub_only'):
        msg += 'in sub-only mode.'
    else:
        msg += 'available for everyone to use (responsibly).'
    await ctx.send(msg)
