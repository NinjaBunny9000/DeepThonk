from config.importer import twitch_cmd_prefix
import os

def list_commands(listyboi):

    msgs = list()
    msg = str()

    for cmd in listyboi:
        if (len(msg) + len(cmd) + 2) < 500:
            msg = msg + f"{twitch_cmd_prefix}{cmd} "
        else:
            msgs.append(msg)
            msg = ""
    if msg:
        msg = msg[:-1]
        msgs.append(msg)

    return msgs

def ok_or_nah(ctx, sub=False, mod=False, streamer=False):
    # check if the author is at least that level or nah

    if sub and (ctx.author.is_subscriber or 'founder' in ctx.author.badges.keys()):
        return False

    elif mod and ctx.author.is_mod: # and author is a mod
        return False

    elif streamer and ctx.author.name.lower() == os.environ['TWITCH_CHANNEL']:
        return False

    else:
        return True

