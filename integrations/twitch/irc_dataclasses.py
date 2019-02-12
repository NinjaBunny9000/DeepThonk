import asyncio
import uuid
import datetime
import inspect
import os

try:
    import isodate
    iso_installed = True
except ImportError:
    print("To use music, please install isodate. (pip install isodate)")
    iso_installed = False

try:
    import aiohttp
    aio_installed = True
except ImportError:
    print("To use stats from the API, make sure to install aiohttp. "
          "(pip install aiohttp)")
    aio_installed = False


def _parse_badges(s):
    if not s:
        return []
    if "," in s:
        # multiple badges
        badges = s.split(",")
        return [Badge(*badge.split("/")) for badge in badges]
    else:
        return [Badge(*s.split("/"))]


def _parse_emotes(s):
    emotelist = []  # 25:8-12 354:14-18
    if not s:
        return []
    if "/" in s:
        # multiple emotes
        emotes = s.split("/")
        for emote in emotes:
            res = emote.split(":")
            emote_id = res[0]
            locations = res[1]
            if "," in locations:
                for loc in locations.split(","):
                    emotelist.append(Emote(emote_id, loc))
            else:
                emotelist.append(Emote(emote_id, locations))
    else:
        res = s.split(":")
        emote_id = res[0]
        locations = res[1]
        if "," in locations:
            for loc in locations.split(","):
                emotelist.append(Emote(emote_id, loc))
        else:
            emotelist.append(Emote(emote_id, locations))
    return emotelist

class Object:
    """
    An object that may be created as substitute for functions.
    """
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

class Emote:
    """
    A class to hold emote data

    Attributes
    ----------
    id : int
        The ID of the emote.
    location : str
        The location of the emote in the message.
    url : str
        The url of the emote.
    """
    def __init__(self, id, loc):
        self.id = int(id)
        self.location = loc
        self.url = "https://static-cdn.jtvnw.net/emoticons/v1/{}/3.0".format(
            id)

    def __str__(self):
        global emotes
        if not aio_installed:
            raise Exception("Please install aiohttp to use this feature")
        else:
            for k, v in emotes.items():
                if v['image_id'] == self.id:
                    return k
            return ""


class Badge:
    """
    A class to hold badge data.

    Attributes
    ----------
    name : str
        Name of the badge.
    value : str
        Variant of the badge.
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "{0.name}/{0.value}".format(self)

    @classmethod
    def from_str(cls, s):
        """ e.g. Moderator/1 """
        n, v = s.split("/")
        return cls(n, v)


class User:
    """ Custom user class """

    def __init__(self, a, channel, tags=None):
        self.name = a
        self.channel = channel
        if tags:
            self.badges = _parse_badges(tags['badges'])
            self.mod = tags['mod']
            self.subscriber = tags['subscriber']
            self.type = tags['user-type']
            try:
                self.turbo = tags['turbo']
                self.id = tags['user-id']
            except:
                pass


class Message:
    """ Custom message object to combine message, author and timestamp """

    def __init__(self, m, a, channel, tags):
        if tags:
            self.raw_timestamp = tags['tmi-sent-ts']
            self.timestamp = datetime.datetime.fromtimestamp(
                int(tags['tmi-sent-ts']) / 1000)
            self.emotes = _parse_emotes(tags['emotes'])
            self.id = uuid.UUID(tags['id'])
            self.room_id = tags['room-id']
        self.content = m
        self.author = User(a, channel, tags)
        self.channel = channel

    def __str__(self):
        return self.content


class Command:
    """ A command class to provide methods we can use with it """

    def __init__(self, bot, comm, desc='', alias=[], admin=False, unprefixed=False, listed=True):
        self.comm = comm
        self.desc = desc
        self.alias = alias
        self.admin = admin
        self.listed = listed
        self.unprefixed = unprefixed
        self.subcommands = {}
        self.bot = bot
        bot.commands[comm] = self
        for a in self.alias:
            bot.commands[a] = self

    def subcommand(self, *args, **kwargs):
        """ Create subcommands """
        return SubCommand(self, *args, **kwargs)

    def __call__(self, func):
        """ Make it able to be a decorator """

        self.func = func

        return self

    @asyncio.coroutine
    def run(self, message):
        """ Does type checking for command arguments """
        args = message.content[len(self.bot.prefix):].split(" ")[1:]

        args_name = inspect.getfullargspec(self.func)[0][1:]

        if len(args) > len(args_name):
            args[len(args_name)-1] = " ".join(args[len(args_name)-1:])

            args = args[:len(args_name)]

        ann = self.func.__annotations__

        for x in range(0, len(args_name)):
            try:
                v = args[x]
                k = args_name[x]

                if not type(v) == ann[k]:
                    try:
                        v = ann[k](v)

                    except Exception:
                        raise TypeError("Invalid type: got {}, {} expected"
                            .format(ann[k].__name__, v.__name__))

                args[x] = v
            except IndexError:
                break

        if len(list(self.subcommands.keys())) > 0:
            try:
                subcomm = args.pop(0).split(" ")[0]
            except Exception:
                yield from self.func(message, *args)
                return
            if subcomm in self.subcommands.keys():
                c = message.content.split(" ")
                c.pop(1)
                message.content = " ".join(c)
                yield from self.subcommands[subcomm].run(message)

            else:
                yield from self.func(message, *args)

        else:
            try:
                yield from self.func(message, *args)
            except TypeError as e:
                if len(args) < len(args_name):
                    raise Exception("Not enough arguments for {}, required arguments: {}"
                        .format(self.comm, ", ".join(args_name)))
                else:
                    raise e


class SubCommand(Command):
    """ Subcommand class """

    def __init__(self, parent, comm, desc, *alias):
        self.comm = comm
        self.parent = parent
        self.subcommands = {}
        parent.subcommands[comm] = self
        for a in alias:
            parent.subcommands[a] = self
