import asynctwitch
# import discord
import conf
import cmd
# import discord_chat
import twitch_chat
# import asyncio

# from discord.ext import commands

def start_twitch():
    # pull in the config var for ze bot!
    print('Starting Twitchbot..')
    bot = conf.twitch_instance
    bot.start()

start_twitch()
# discord_chat.start_discord()