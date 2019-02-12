import asyncio
import traceback
import sys
import os
import re
import math
import json
import configparser
import time
import subprocess
import functools
import sqlite3
import pathlib

from .irc_dataclasses import Command, Message, User

# Test if they have aiohttp installed in case they didn't use setup.py
try:
    import aiohttp
    aio_installed = True
except ImportError:
    print("To use stats from the API, make sure to install aiohttp. "
          "(pip install aiohttp)")

    aio_installed = False


@asyncio.coroutine
def _get_url(loop, url):
    session = aiohttp.ClientSession(loop=loop)
    with aiohttp.Timeout(10):
        response = yield from session.get(url)
        try:
            # other statements
            return (yield from response.json())
        finally:
            if sys.exc_info()[0] is not None:
                # on exceptions, close the connection altogether
                response.close()
            else:
                yield from response.release()
            session.close()


def _decrease_msgcount(self):
    self.message_count -= 1


def create_timer(message, channel, time):
    @asyncio.coroutine
    def wrapper(self):
        while True:
            yield from asyncio.sleep(time)
            yield from self.say(channel, message)
    return wrapper


def ratelimit_wrapper(coro):
    @asyncio.coroutine
    def wrapper(self, *args, **kwargs):
        max = 100 if self.is_mod else 20

        while self.message_count == max:
            yield from asyncio.sleep(1)

        self.message_count += 1
        r = yield from coro(self, *args, **kwargs)
        # make sure it doesn't block the event loop
        self.loop.call_later(20, _decrease_msgcount, self)
        return r
    return wrapper


class Bot:
    """
    A basic Bot. All others inherit from this.
    
    Parameters
    ----------
    oauth : str
        The oauth code for your account
    user : str
        Your username
    prefix : Optional[str]
        The prefix for the bot to listen to. (default: `!`)
    channel : Optional[str, list]
        The channel(s) to serve. (default: `twitch`)
    client_id : Optional[str]
        The application Client ID for the kraken API.
    cache : Optional[int]
        The amount of messages to cache. (default: 100)
    admins : Optional[list]
        The usernames with full access to the bot.
    allow_streams : Optional[bool]
        Allow music to play continuous streams
    """

    def __init__(self, **kwargs):

        if kwargs.get("config"):
            self.load(kwargs.get("config"))

        else:
            self.prefix = kwargs.get("prefix") or "!"
            self.oauth = kwargs.get("oauth")
            self.nick = kwargs.get("user").lower()
            channel = kwargs.get("channel") or "twitch"
            if isinstance(channel, str):
                self.chan = ["#" + channel.lower().strip('#')]
            else:
                self.chan = ["#" + c.lower().strip('#') for c in channel]
            self.client_id = kwargs.get("client_id")

        if os.name == 'nt':
            self.loop = asyncio.ProactorEventLoop()
        else:
            self.loop = asyncio.get_event_loop()

        self.cache_length = kwargs.get("cache") or 100

        asyncio.set_event_loop(self.loop)
        self.host_url = "irc.chat.twitch.tv"
        self.port = 6667

        self.admins = kwargs.get("admins") or []

        self.is_mod = False
        self.allow_streams = kwargs.get("allow_streams")

        # Just in case some get sent almost simultaneously even though they
        # shouldn't, limit the message count to max-1
        self.message_count = 1

        self.regex = {
            "data": re.compile(
                r"^(?:@(?P<tags>\S+)\s)?:(?P<data>\S+)(?:\s)"
                r"(?P<action>[A-Z]+)(?:\s#)(?P<channel>\S+)"
                r"(?:\s(?::)?(?P<content>.+))?"),
            "ping": re.compile(r"PING (?P<content>.+)"),
            "author": re.compile(
                r"(?P<author>[a-zA-Z0-9_]+)!(?P=author)"
                r"@(?P=author).tmi.twitch.tv"),
            "mode": re.compile(r"(?P<mode>[\+\-])o (?P<user>.+)"),
            "host": re.compile(
                r"(?P<channel>[a-zA-Z0-9_]+) "
                r"(?P<count>[0-9\-]+)")}

        self.channel_stats = {}

        self.viewer_count = {}
        self.host_count = {}

        self.viewers = {}

        self.hosts = {}

        self.messages = []
        self.channel_moderators = {}
            
        for c in self.chan:
            self.channel_stats[c] = {}

            self.viewer_count[c] = 0
            self.host_count[c] = 0

            self.viewers[c] = {}

            self.hosts[c] = []

            self.channel_moderators[c] = []

    def debug(self):
        for x, y in self.__dict__.items():
            print(x, y)

    def load(self, path):
        """
        Load settings from a config file.
        
        Parameters
        ----------
        path : str
            path to the config file

        """
        config = configparser.ConfigParser(interpolation=None)
        config.read(path)
        self.oauth = config.get("Settings", "oauth", fallback=None)
        self.nick = config.get("Settings", "username", fallback=None)
        self.chan = "#" + config.get("Settings", "channel", fallback="twitch")
        self.prefix = config.get("Settings", "prefix", fallback="!")
        self.client_id = config.get("Settings", "client_id", fallback=None)

    def override(self, coro):
        """
        Decorator function to override events.

        .. code-block:: python

            @bot.override
            async def event_message(message):
                print(message.content)

        """
        if 'event' not in coro.__name__:
            raise Exception(
                "Accepted overrides start with 'event_' or 'raw_event'")
        setattr(self, coro.__name__, coro)

    @asyncio.coroutine
    def _get_stats(self):
        """ Gets JSON from the Kraken API """
        if not aio_installed:
            return

        global emotes
        emotes = (yield from _get_url(
            self.loop,
            "https://twitchemotes.com/api_cache/v3/global.json"))

        if not self.client_id:
            return

        while True:
            try:
                for c in self.chan:
                    j = yield from _get_url(
                        self.loop,
                        'https://api.twitch.tv/kraken/channels/{}?client_id={}'
                        .format(c[1:], self.client_id))
                    self.channel_stats[c] = {
                        'mature': j['mature'],
                        'title': j['status'],
                        'game': j['game'],
                        'id': j['_id'],
                        'created_at': time.mktime(
                            time.strptime(
                                j['created_at'],
                                '%Y-%m-%dT%H:%M:%SZ')),
                        'updated_at': time.mktime(
                            time.strptime(
                                j['updated_at'],
                                '%Y-%m-%dT%H:%M:%SZ')),
                        'delay': j['delay'],
                        'offline_logo': j['video_banner'],
                        'profile_picture': j['logo'],
                        'profile_banner': j['profile_banner'],
                        'twitch_partner': j['partner'],
                        'views': j['views'],
                        'followers': j['followers']}

                    j = yield from _get_url(
                        self.loop,
                        'https://tmi.twitch.tv/hosts?target={}&include_logins=1'
                        .format(j['_id']))
                    self.host_count[c] = len(j['hosts'])
                    self.hosts[c] = [x['host_login'] for x in j['hosts']]

                    j = yield from _get_url(
                        self.loop,
                        'https://tmi.twitch.tv/group/user/{}/chatters'
                        .format(c[1:]))
                    self.viewer_count[c] = j['chatter_count']
                    self.channel_moderators[c] = j['chatters']['moderators']
                    self.viewers[c]['viewers'] = j['chatters']['viewers']
                    self.viewers[c]['moderators'] = j['chatters']['moderators']
                    self.viewers[c]['staff'] = j['chatters']['staff']
                    self.viewers[c]['admins'] = j['chatters']['admins']
                    self.viewers[c]['global_moderators'] = j[
                        'chatters']['global_mods']

            except Exception:
                # traceback.print_exc()
                print('YA DUN GOOFED')
                pass
            yield from asyncio.sleep(60)

    @asyncio.coroutine
    def _pong(self, src):
        """ Tell remote we're still alive """
        self.writer.write("PONG {}\r\n".format(src).encode('utf-8'))


    def start(self, tasked=False):
        """
        Starts the bot.
        
        Parameters
        ----------
        tasked : Optional[bool]
            Creates a task on the bot loop if True. (default: False)
        """
        if self.client_id is not None:
            self.loop.create_task(self._get_stats())
        if tasked:
            self.loop.create_task(self._tcp_echo_client())
        else:
            self.loop.run_until_complete(self._tcp_echo_client())
            

    @asyncio.coroutine
    @ratelimit_wrapper
    def say(self, channel, message):
        """
        Send a message to the specified channel.
        
        Parameters
        ----------
        channel : str
            The channel to send the message to.
        message : str
            The message to send.
        """

        if len(message) > 500:
            raise Exception(
                "The maximum amount of characters in one message is 500,"
                " you tried to send {} characters".format(
                    len(message)))

        while message.startswith("."):  # Use Bot.ban, Bot.timeout, etc instead
            message = message[1:]

        yield from self._send_privmsg(channel, message)

    @asyncio.coroutine
    def _nick(self):
        """ Send name """
        self.writer.write("NICK {}\r\n".format(self.nick).encode('utf-8'))

    @asyncio.coroutine
    def _pass(self):
        """ Send oauth token """
        self.writer.write("PASS {}\r\n".format(self.oauth).encode('utf-8'))

    @asyncio.coroutine
    def _join(self, channel):
        """ Join a channel """
        self.writer.write("JOIN {}\r\n".format(channel).encode('utf-8'))

    @asyncio.coroutine
    def _part(self, channel):
        """ Leave a channel """
        self.writer.write("PART #{}\r\n".format(channel).encode('utf-8'))

    @asyncio.coroutine
    def _special(self, mode):
        """ Allows for more events """
        self.writer.write(
            bytes("CAP REQ :twitch.tv/{}\r\n".format(mode), "UTF-8"))

    @asyncio.coroutine
    def _cache(self, message):
        self.messages.append(message)
        if len(self.messages) > self.cache_length:
            self.messages.pop(0)

    @asyncio.coroutine
    def _send_privmsg(self, channel, s):
        """ DO NOT USE THIS YOURSELF OR YOU RISK GETTING BANNED FROM TWITCH """
        s = s.replace("\n", " ")
        self.writer.write("PRIVMSG #{} :{}\r\n".format(
            channel, s).encode('utf-8'))

 
    @asyncio.coroutine
    @ratelimit_wrapper
    def ban(self, user, reason=''):
        """
        Ban a user.
        
        Parameters
        ----------
        user : :class:`User`
            The user to ban.
        reason : Optional[str]
            The reason a user was banned.
        """
        yield from self._send_privmsg(user.channel, ".ban {} {}".format(user.name, reason))

    @asyncio.coroutine
    @ratelimit_wrapper
    def unban(self, user):
        """
        Unban a banned user
        
        Parameters
        ----------
        user : :class:`User`
            The user to unban.
        """
        yield from self._send_privmsg(user.channel, ".unban {}".format(user.name))

    @asyncio.coroutine
    @ratelimit_wrapper
    def timeout(self, user, seconds=600, reason=''):
        """
        Timeout a user.
        
        Parameters
        ----------
        user : :class:`User`
            The user to time out.
        seconds : Optional[int]
            The amount of seconds to timeout for.
        reason : Optional[str]
            The reason a user was timed out.
        """
        yield from self._send_privmsg(user.channel, ".timeout {} {} {}".format(
                                                                 user.name, seconds,
                                                                 reason))

    @asyncio.coroutine
    @ratelimit_wrapper
    def me(self, channel, text):
        """
        The /me command.
        
        Parameters
        ----------
        channel : str
            The channel to use /me in.
        text : str
            The text to use in /me.
        """
        yield from self._send_privmsg(channel, ".me {}".format(text))

    @asyncio.coroutine
    @ratelimit_wrapper
    def whisper(self, user, message):
        """
        Send a private message to a user
        
        Parameters
        ----------
        user : :class:`User`
            The user to send a message to.
        message : str
            The message to send.
        """
        yield from self._send_privmsg(user.channel, ".w {} {}".format(user.name, message))


    @asyncio.coroutine
    @ratelimit_wrapper
    def mod(self, user):
        """
        Give moderator status to a user.
        
        Parameters
        ----------
        user : :class:`User`
            The user to give moderator.
        """
        yield from self._send_privmsg(user.channel, ".mod {}".format(user.name))

    @asyncio.coroutine
    @ratelimit_wrapper
    def unmod(self, user):
        """
        Remove moderator status from a user.
        
        Parameters
        ----------
        user : :class:`User`
            The user to remove moderator from.
        """
        yield from self._send_privmsg(user.channel, ".unmod {}".format(user.name))

    @asyncio.coroutine
    @ratelimit_wrapper
    def clear(self, channel):
        """
        Clear a channel.
        
        Parameters
        ----------
        channel : str
            The channel to clear.
        """
        yield from self._send_privmsg(channel, ".clear")

    @asyncio.coroutine
    @ratelimit_wrapper
    def subscribers_on(self, channel):
        """
        Set channel mode to subscribers only.
        
        Parameters
        ----------
        channel : str
            The channel to enable this on.
        """
        yield from self._send_privmsg(channel, ".subscribers")

    @asyncio.coroutine
    @ratelimit_wrapper
    def subscribers_off(self, channel):
        """
        Unset channel mode to subscribers only.
        
        Parameters
        ----------
        channel : str
            The channel to disable this on.
        """
        yield from self._send_privmsg(channel, ".subscribersoff")

    @asyncio.coroutine
    @ratelimit_wrapper
    def slow_on(self, channel):
        """
        Set channel mode to slowmode.
        
        Parameters
        ----------
        channel : str
            The channel to enable this on.
        """
        yield from self._send_privmsg(channel, ".slow")

    @asyncio.coroutine
    @ratelimit_wrapper
    def slow_off(self, channel):
        """
        Unset channel mode to slowmode.
        
        Parameters
        ----------
        channel : str
            The channel to disable this on.
        """
        yield from self._send_privmsg(channel, ".slowoff")

    @asyncio.coroutine
    @ratelimit_wrapper
    def r9k_on(self, channel):
        """
        Set channel mode to r9k.
        
        Parameters
        ----------
        channel : str
            The channel to enable this on.
        """
        yield from self._send_privmsg(channel, ".r9k")

    @asyncio.coroutine
    @ratelimit_wrapper
    def r9k_off(self, channel):
        """
        Unset channel mode to r9k.
        
        Parameters
        ----------
        channel : str
            The channel to enable this on.
        """
        yield from self._send_privmsg(channel, ".r9koff")

    @asyncio.coroutine
    @ratelimit_wrapper
    def emote_only_on(self, channel):
        """
        Set channel mode to emote-only.
        
        Parameters
        ----------
        channel : str
            The channel to enable this on.
        """
        yield from self._send_privmsg(channel, ".emoteonly")

    @asyncio.coroutine
    @ratelimit_wrapper
    def emote_only_off(self, channel):
        """
        Unset channel mode to emote-only.
        
        Parameters
        ----------
        channel : str
            The channel to disable this on.
        """
        yield from self._send_privmsg(channel, ".emoteonlyoff")

    @asyncio.coroutine
    @ratelimit_wrapper
    def host(self, channel, user):
        """
        Start hosting a channel.
        
        Parameters
        ----------
        channel : str
            The channel that will be hosting.
        user : str
            The channel to host.
        """
        yield from self._send_privmsg(channel, ".host {}".format(user))

    @asyncio.coroutine
    @ratelimit_wrapper
    def unhost(self, channel):
        """
        Stop hosting a channel.
        
        Parameters
        ----------
        channel : str
            The channel that was hosting.
        """
        yield from self._send_privmsg(channel, ".unhost")

    # End of Twitch commands

    @asyncio.coroutine
    def _tcp_echo_client(self):
        """ Receive events and trigger events """

        self.reader, self.writer = yield from asyncio.open_connection(
            self.host_url, self.port, loop=self.loop)

        if not self.nick.startswith('justinfan'):
            yield from self._pass()
        yield from self._nick()

        modes = ("commands", "tags", "membership")
        for m in modes:
            yield from self._special(m)

        for c in self.chan:
            yield from self._join(c)

        while True:
            rdata = (yield from self.reader.readline()).decode("utf-8").strip()

            if not rdata:
                continue

            yield from self.raw_event(rdata)

            try:

                if rdata.startswith("PING"):
                    p = self.regex["ping"]

                else:
                    p = self.regex["data"]

                m = p.match(rdata)

                try:
                    tags = m.group("tags")

                    tagdict = {}
                    for tag in tags.split(";"):
                        t = tag.split("=")
                        if t[1].isnumeric():
                            t[1] = int(t[1])
                        tagdict[t[0]] = t[1]
                    tags = tagdict
                except:
                    tags = None

                try:
                    action = m.group("action")
                except:
                    action = "PING"

                try:
                    data = m.group("data")
                except:
                    data = None

                try:
                    content = m.group('content')
                except:
                    content = None

                try:
                    channel = m.group('channel')
                except:
                    channel = None

            except:
                pass

            else:
                try:
                    if not action:
                        continue

                    if action == "PING":
                        yield from self._pong(content)

                    elif action == "PRIVMSG":
                        sender = self.regex["author"].match(
                            data).group("author")

                        messageobj = Message(content, sender, channel, tags)

                        yield from self._cache(messageobj)

                        yield from self.event_message(messageobj)

                    elif action == "WHISPER":
                        sender = self.regex["author"].match(
                            data).group("author")

                        messageobj = Message(content, sender, channel, tags)

                        yield from self._cache(messageobj)

                        yield from self.event_private_message(messageobj)

                    elif action == "JOIN":
                        sender = self.regex["author"].match(
                            data).group("author")

                        yield from self.event_user_join(User(sender, channel))

                    elif action == "PART":
                        sender = self.regex["author"].match(
                            data).group("author")

                        yield from self.event_user_leave(User(sender, channel))

                    elif action == "MODE":

                        m = self.regex["mode"].match(content)
                        mode = m.group("mode")
                        user = m.group("user")

                        if mode == "+":
                            yield from self.event_user_op(User(user, channel))
                        else:
                            yield from self.event_user_deop(User(user, channel))

                    elif action == "USERSTATE":

                        if tags["mod"] == 1:
                            self.is_mod = True
                        else:
                            self.is_mod = False

                        yield from self.event_userstate(User(self.nick, channel, tags))

                    elif action == "ROOMSTATE":
                        yield from self.event_roomstate(channel, tags)

                    elif action == "NOTICE":
                        yield from self.event_notice(channel, tags)

                    elif action == "CLEARCHAT":
                        if not content:
                            yield from self.event_clear(channel)
                        else:
                            if "ban-duration" in tags.keys():
                                yield from self.event_timeout(
                                    User(content, channel), tags)
                            else:
                                yield from self.event_ban(
                                    User(content, channel), tags)

                    elif action == "HOSTTARGET":
                        m = self.regex["host"].match(content)
                        hchannel = m.group("channel")
                        viewers = m.group("count")

                        if channel == "-":
                            yield from self.event_host_stop(channel, viewers)
                        else:
                            yield from self.event_host_start(channel, hchannel, viewers)

                    elif action == "USERNOTICE":
                        message = content or ""
                        user = tags["login"]

                        yield from self.event_subscribe(
                            Message(message, user, channel, tags), tags)

                    elif action == "CAP":
                        # We don"t need this for anything, so just ignore it
                        continue

                    else:
                        print("Unknown event:", action)
                        print(rdata)

                except Exception as e:
                    yield from self.parse_error(e)

    # Events called by TCP connection

    @asyncio.coroutine
    def event_notice(self, channel, tags):
        """
        Called on NOTICE events (when commands are called).
        """
        pass

    @asyncio.coroutine
    def event_clear(self, channel):
        """
        Called when chat is cleared by someone else.
        """
        pass

    @asyncio.coroutine
    def event_subscribe(self, message, tags):
        """
        Called when someone (re-)subscribes.
        """
        pass

    @asyncio.coroutine
    def event_host_start(self, channel, hosted_channel, viewer_count):
        """
        Called when the streamer starts hosting.
        """
        pass

    @asyncio.coroutine
    def event_host_stop(self, channel, viewercount):
        """
        Called when the streamer stops hosting.
        """
        pass

    @asyncio.coroutine
    def event_ban(self, user, tags):
        """
        Called when a user is banned.
        """
        pass

    @asyncio.coroutine
    def event_timeout(self, user, tags):
        """
        Called when a user is timed out.
        """
        pass

    @asyncio.coroutine
    def event_roomstate(self, channel, tags):
        """
        Triggered when a channel's chat settings change.
        """
        pass

    @asyncio.coroutine
    def event_userstate(self, user):
        """
        Triggered when the bot sends a message.
        """
        pass

    @asyncio.coroutine
    def raw_event(self, data):
        """
        Called on all events after event_ready.
        """
        pass

    @asyncio.coroutine
    def event_user_join(self, user):
        """
        Called when a user joins a channel.
        """
        pass

    @asyncio.coroutine
    def event_user_leave(self, user):
        """
        Called when a user leaves a channel.
        """
        pass

    @asyncio.coroutine
    def event_user_deop(self, user):
        """
        Called when a user is de-opped.
        """
        pass

    @asyncio.coroutine
    def event_user_op(self, user):
        """
        Called when a user is opped.
        """
        pass

    @asyncio.coroutine
    def event_private_message(self, message):
        """
        Called when the bot receives a private message.
        """
        pass

    @asyncio.coroutine
    def event_message(self, message):
        """
        Called when a message is sent by someone in chat.
        """
        pass

    # End of events

    def stop(self, exit=False):
        """
        Stops the bot and disables using it again.
        
        Parameters
        ----------
        exit : Optional[bool]
            If True, this will close the event loop and raise SystemExit. (default: False)
        """

        # if hasattr(self, "player"):
        #     self.player.terminate()

        if hasattr(self, "writer"):
            self.writer.close()

        pending = asyncio.Task.all_tasks()
        gathered = asyncio.gather(*pending)

        try:
            gathered.cancel()
            self.loop.run_until_complete(gathered)
            gathered.exception()
        except:  # Can be ignored
            pass

        if exit:
            self.loop.stop()
            sys.exit(0)

    @asyncio.coroutine
    def parse_error(self, e):
        """
        Called when something errors.
        """

        fname = e.__traceback__.tb_next.tb_frame.f_code.co_name
        print("Ignoring exception in {}:".format(fname))
        traceback.print_exc()


class CommandBot(Bot):
    """
    Allows the usage of Commands more easily
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = {}

    @asyncio.coroutine
    def event_message(self, m):
        """
        If you override this function, make sure to yield from/await `CommandBot.parse_commands`
        """
        yield from self.parse_commands(m)

    @asyncio.coroutine
    def parse_commands(self, rm):
        """
        The command parser. It is not recommended to override this.
        """

        if self.nick == rm.author.name:
            return
        
        if rm.content.startswith(self.prefix):

            m = rm.content[len(self.prefix):]
            cl = m.split(" ")
            w = cl.pop(0).lower().replace("\r", "")
            m = " ".join(cl)
 
            if w in self.commands:
                if not self.commands[w].unprefixed:
                    if self.commands[w].admin and rm.author.name not in self.admins:
                        yield from self.say(self.chan,
                            "You are not allowed to use this command")
                    yield from self.commands[w].run(rm)

        else:
            cl = rm.content.split(" ")
            w = cl.pop(0).lower()

            if w in self.commands:
                if self.commands[w].unprefixed == True:
                    yield from self.commands[w].run(rm)

    def command(*args, **kwargs):
        """
        A decorator to add a command.
        see :ref:`Command` for usage.
        """
        return Command(*args, **kwargs)

    def add_timer(self, channel, message, time=60):
        """
        Send a message on a timer.
        
        Parameters
        ----------
        channel : str
            The channel to send the message to.
        message: str
            The message to send.
        time : Optional[int]
            The interval to send the message. (default: 60)
        """
        t = create_timer(message, channel, time)
        self.loop.create_task(t(self))