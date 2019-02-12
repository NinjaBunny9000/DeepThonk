import conf
from integrations.twitch.api_wrapper import get_mods
import integrations.twitch.irc_dataclasses

def is_mod(user):
    if isinstance(user, integrations.twitch.irc_dataclasses.Message):
        if (user.author.mod or user.author.name.lower() == conf.streamer.lower()):
            return True
    elif user in get_mods():
        return True
    else:
        return False


def is_bot(message):
    if (message.author.name.lower() in str(conf.bot_list).lower()):
        return True
    else:
        return False

