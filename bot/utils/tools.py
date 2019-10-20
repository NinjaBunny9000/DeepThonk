from config.importer import twitch_cmd_prefix

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
        msg = msg[:-2]
        msgs.append(msg)

    return msgs