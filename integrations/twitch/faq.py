# internal modules & packages
import conf
import data_tools
import content
from sfx.sfx import play_sfx
from integrations.twitch.privilege import is_mod

# config ze bot!
twitch_bot = conf.twitch_instance
welcome_msg_sent = 0


# ANCHOR  Help Command
###############################################################################

help_commands = conf.bot_settings['help_cmds']

@twitch_bot.command('help', alias=help_commands)
async def cmd(message):
    play_sfx('sfx/help.mp3')
    await twitch_bot.say(message.channel, content.help_menu(message))


# ANCHOR  Misc FAQ Commands
###############################################################################

# globals everyone can bitch about
branch_url = 'https://github.com/NinjaBunny9000/DeepThonk/tree/beta-refactor' # TODO move to db
repo_url = 'https://github.com/NinjaBunny9000/DeepThonk/'


@twitch_bot.command('branch', alias=['current'])
async def branch(message):
    token = data_tools.tokenize(message, 1)
    global branch_url
    
    if is_mod(message) and len(token) == 2:
        branch_url = token[1]
        msg = f'New branch set to \"{branch_url}\"'
        await twitch_bot.say(message.channel, msg)
    else:
        msg = f"The branch Bun's working in rn is: {branch_url}"
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('repo', alias=['repository', 'suppository'])
async def repo(message):
    token = data_tools.tokenize(message, 1)
    global repo_url
    
    if is_mod(message) and len(token) == 2:
        repo_url = token[1]
        msg = f'New project repo set to \"{repo_url}\"'
        await twitch_bot.say(message.channel, msg)
    else:
        msg = f"The repo Bun's working with rn is: {repo_url}"
        await twitch_bot.say(message.channel, msg)
