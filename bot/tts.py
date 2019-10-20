
from config.importer import bot
from server_interface import emit_tts
from utils.logger import loggymclogger as log

log.debug(f"{__name__} loaded")

tts_on = True
tts_sub_only = False


@bot.command(name='ttson')
async def ttson(ctx):
    if ctx.author.is_mod is False:
        return
    global tts_on
    if tts_on is False:
        tts_on = True
        await ctx.send(f"TTS turned back on..")
    else:
        await ctx.send(f"TTS is already on.")


@bot.command(name='ttsoff')
async def ttsoff(ctx):
    if ctx.author.is_mod is False:
        return
    global tts_on
    if tts_on is True:
        tts_on = False
        await ctx.send(f"TTS temporarily disabled.")
    else:
        await ctx.send(f"TTS is already off.")


@bot.command(name='ttssub')
async def ttssub(ctx):
    'Toggle TTS being sub-only or nah'
    if ctx.author.is_mod is False:
        return
    global tts_sub_only
    tts_sub_only = not tts_sub_only
    msg = f"TTS is now "
    if tts_sub_only is True:
        msg += "in sub-only mode."
    else:
        msg += "free for everyone to use (responsibly)."
    await ctx.send(msg)


@bot.command(name='ttsmode')
async def ttsmode(ctx):
    'Reports who can use TTS in chat.'
    msg = 'TTS are '
    if tts_sub_only:
        msg += 'in sub-only mode.'
    else:
        msg += "available for everyone to use (responsibly)."
    await ctx.send(msg)


@bot.command(name='tts')
async def tts(ctx):
    'Lets chat use TTS w/o cheers or other events.'
    if tts_on is False:
        await ctx.send(f"@{ctx.author.name} => TTS is temporarily disabled.")
        return

    if tts_sub_only and (ctx.author.subscriber is False or ctx.author.is_mod is False):
        await ctx.send(f'@{ctx.author.name} => TTS is sub-only during IRL streams.')
        return
    print(ctx.content)
    token = ctx.content.split(' ',1)
    await emit_tts(token[1])
    log.debug(f'tts request detected in chat: {token[1]}')