import os
import socket
import asyncio
from threading import Thread
from logger import log
from dearpygui import core, simple
from dearpygui.core import log_info, log_debug, log_error, log_warning, clear_log
import re
from typing import Callable, Dict, List

# from twitchbot import Command


# @Command('COMMAND_NAME')
# async def cmd_function(msg, *args):
#     await msg.reply('i was called!')

class Message:

    def __init__(self):
        self.channel = os.getenv('TWITCH_CHANNEL')  # todo eventually handle multiple channels
        self.author = str()
        self.content = str()

    async def parse(self, response):

        # handle diff types of messages
        if 'PRIVMSG' in response:
            log_debug(f'(raw) {response}')
            split = response.split('PRIVMSG', 1)
            # self.content = re.split(r':|@|!|.tmi.twitch.tv', split[0].replace(' ', ''))
            self.author = re.split(r':|@|!|.tmi.twitch.tv', split[0])[1]
            self.content = split[1].strip('\r\n').split(f" #{self.channel} :", 1)[1]
            # log_info(str(self))
            return self
        else:
            pass
            # log_debug(response)

    def __str__(self):
        return f"#{self.channel}@{self.author}: {self.content}"


class Command:

    registered = {}

    def __init__(self, name, func: Callable = None, aliases: List[str] = None):
        self.prefix = '!'  # todo add this to env vars
        self.name = name
        self.aliases = aliases
        self.func = func
        Command.registered[f"{self.prefix}{self.name}"] = self
        if self.aliases:
            for alias in self.aliases:
                Command.registered[f"{self.prefix}{alias}"] = self


    def __call__(self, func) -> 'Command':
        log_debug(self.name)
        self.func = func
        return self


class IRCInterface:

    def __init__(self):
        self.socket = socket.socket()

    async def _connect(self):
        log.debug('logging in')
        self.socket.connect(('irc.chat.twitch.tv', 80))
        self.socket.send(f"PASS {os.getenv('TWITCH_TOKEN')}\n".encode('utf-8'))
        self.socket.send(f"NICK {os.getenv('TWITCH_BOT_NICK')}\n".encode('utf-8'))
        self.socket.send(f"JOIN #{os.getenv('TWITCH_CHANNEL')}\n".encode('utf-8'))

    async def _recieve(self) -> Message:
        while True:
            response = self.socket.recv(2048).decode('utf-8')
            if response:
                return await Message().parse(response)

    async def send(self, msg):
        self.socket.send(f"PRIVMSG #{os.getenv('TWITCH_CHANNEL')} :{msg}\r\n".encode('utf-8'))




class Bot(IRCInterface):

    def __init__(self):
        super(Bot, self).__init__()
        self.online = False
        self.msg = None
        self.command = Command
        self.commands = Command.registered

    async def bigloop(self):
        log.debug('bot online?')
        self.online = True
        await self._connect()
        await self._listen()


        # TODO swap to .env and generate .env as well as settings.json
        # TODO directory for command scripts to live would be tight
        # read in config data
        # initialize the bot (load settings, commands, etc)
        # connect to twitch

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.bigloop())

    def run_thread(self) -> Thread:
        thread = Thread(target=self.run, name='bot_thread')
        thread.start()
        return thread

    async def _listen(self):
        while self.online:
            self.msg = await self._recieve()


            # TODO this is patchwork until we can recognize all types of msgs from twitch, not just PRIVMSG
            # ignore msgs that aren't PRIVMSG
            if self.msg is None:
                continue

            log_info(str(self.msg))
            if self.msg.content in Command.registered.keys():
                cmd = self.msg.content.split(' ')[0]
                log_debug(cmd)
                await Command.registered[cmd].func()





