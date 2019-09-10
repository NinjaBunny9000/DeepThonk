""" Chat commands used in interfacing with the IRL robot

Utilizes the TwitchIO lib to connect chat to the IRL robot interface
(using websockets).
"""

from config.importer import bot
from robo_interface import emit_expression
from utils.logger import loggymclogger as log

log.debug(f"{__name__} loaded")

@bot.command(name='tantrum')
async def tantrum(ctx):
    await emit_expression('tantrum')
    msg = f'WAHHHHHHHHHHHHHHHHHHH'
    await ctx.send(msg)
    msg = f'/me flails about'
    await ctx.send(msg)


@bot.command(name='gasp')
async def gasp(ctx):
    await emit_expression('gasp')
    log.debug('Deepthonk gasped!')


@bot.command(name='snore')
async def snore(ctx):
    await emit_expression('snore')
    log.debug('Deepthonk is snoring.')


@bot.command(name='playdead')
async def playdead(ctx):
    await emit_expression('playdead')
    log.debug('Deepthonk is playing dead!')


@bot.command(name='dance')
async def dance(ctx):
    await emit_expression('dance')
    log.debug('Deepthonk is gettin it\'s groove on.')


@bot.command(name='rave')
async def rave(ctx):
    await emit_expression('rave')
    log.debug('Deepthonk goin ham at the rave. UNCE UNCE UNCE')


@bot.command(name='lul')
async def lul(ctx):
    await emit_expression('lul')
    log.debug('Deepthonk lulled.')


@bot.command(name='yee')
async def yee(ctx):
    await emit_expression('yee')
    log.debug('Deepthonk agrees.')


@bot.command(name='nah')
async def nah(ctx):
    await emit_expression('nah')
    log.debug('Deepthonk disagrees.')
