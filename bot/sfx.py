"""Creates sfx commands and triggers SFX on server."""

from config.importer import bot
from server_interface import emit_sfx
from utils.logger import loggymclogger as log
from utils.tools import list_commands

log.debug(f"{__name__} loaded")


sfx_state = True
sfx_sub_only = False


@bot.command(name='sfxon')
async def sfxon(ctx):
    if ctx.author.is_mod is False:
        return
    global sfx_state

    if sfx_state:
        await ctx.send(f"@{ctx.author.name} => SFX are already on.")
    else:
        sfx_state = True
        await ctx.send(f"@{ctx.author.name} => SFX are on now.")


@bot.command(name='sfxoff')
async def sfxoff(ctx):
    if ctx.author.is_mod is False:
        return
    global sfx_state
    
    if not sfx_state:
        await ctx.send(f"@{ctx.author.name} => SFX are already off.")
    else:
        sfx_state = False
        await ctx.send(f"@{ctx.author.name} => SFX are disabled now.")


@bot.command(name='sfxtoggle')
async def sfxtoggle(ctx):
    if ctx.author.is_mod is False:
        return
    global sfx_state
    sfx_state = not sfx_state


@bot.command(name='sfxsub')
async def sfxsub(ctx):
    'Make SFX for subs-only or nah.'
    if ctx.author.is_mod is False:
        return
    global sfx_sub_only
    sfx_sub_only = not sfx_sub_only
    msg = f"SFX are now "
    if sfx_sub_only is True:
        msg += 'in sub-only mode.'
    else:
        msg += "available for everyone to use (responsibly)."
    await ctx.send(msg)


@bot.command(name='sfxmode')
async def sfxmode(ctx):
    'Reports to chat what mode SFX are in.'
    msg = 'SFX are '
    if sfx_sub_only:
        msg += 'in sub-only mode.'
    else:
        msg += "available for everyone to use (responsibly)."
    await ctx.send(msg)


class SoundEffect:
    'Instangenitals all the SFX commands, based on files on the server.'

    commands = []

    def __init__(self, cmd_name_with_extenion):
        cmd_no_extension = cmd_name_with_extenion[:-4] 
        SoundEffect.commands.append(cmd_no_extension) # list of sfx cmds
        # log.debug(f"SFX {cmd_no_extension} created.")
        
        # create/register file as command in event-loop
        @bot.command(name=cmd_no_extension)
        async def sfx_func(ctx):
            
            if sfx_state is False:
                await ctx.send(f"@{ctx.author.name} => SFX are temporarily disabled.")
                return

            if sfx_sub_only and (ctx.author.subscriber is False or ctx.author.is_mod is False):
                await ctx.send(f'@{ctx.author.name} => SFX are sub-only at the moment.')
                return

            await emit_sfx(cmd_name_with_extenion)  # send the command to the server

            log.debug(f'SFX request detected in chat: {cmd_no_extension}')

    def generate_sfx_list():
        'generates a list of sfx commands once the websocket is recieved and commands are generated'

        @bot.command(name='sfx')
        async def sfx(ctx):

            await emit_sfx('murderbot')

            commands = list_commands(SoundEffect.commands)

            for msg in commands:
                await ctx.send(msg)

           


