import os
from twitchbot import BaseBot, Message
from dearpygui import core, simple
from logger import log
import socket
import json
from emoji import demojize, emojize
from config import Config
from dearpygui.core import log_info, log_debug, log_error, log_warning, clear_log

from bot import Bot, Command
# demojize()

# ignore this cuz i suck
if os.getenv('TWITCH_BOT_NICK'):
    print('SUCCESS')

cfg = Config()

class DeepThonk(BaseBot):

    def __init__(self):
        super(DeepThonk, self).__init__()
        self.online = False

    # override events here
    async def on_privmsg_received(self, msg: Message) -> None:
        print(f'[{msg.channel_name}] {msg.author} sent: {msg.content}')

# bot = DeepThonk()

bot = Bot()

@bot.command('test', aliases=['testicles'])
async def test():
    log_debug('IT WORKED')

log_info(bot.commands)



# things we want to be able to see in the gui
    # sfx list w/buttons
    # add/remove commands
    # add/remove faq
    # restart the bot
    # enable/disable different modules
    # buttons for top features
    # display bot status

# GUI STUFFS
core.show_logger()
core.set_main_window_size(width=800, height=500)
core.set_main_window_title('DeepThonk')






with simple.window('Main', ):
    with simple.menu_bar('Main Menu Bar'):
        with simple.menu('File'):
            core.add_menu_item('Settings')
        core.add_menu_item('STATUS: Online')
        core.add_menu_item('STATUS: Offline')
        simple.hide_item('STATUS: Online')
        core.add_menu_item('Restart')


def startBot(sender, data):
    bot.run_thread()
    simple.hide_item('STATUS: Offline')
    simple.show_item('STATUS: Online')


with simple.window('Bot Controls', x_pos=0, y_pos=20):
    core.add_button('Start', callback=startBot)
    core.add_button('Close', callback=lambda:quit())



core.start_dearpygui(primary_window='Main')

