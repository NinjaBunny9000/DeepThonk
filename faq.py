from conf import twitch_instance, twitch_channel, streamer, welcome_msg
from permissions import is_bot, is_mod
import data_tools
import content

# config ze bot!
twitch_bot = twitch_instance
welcome_msg_sent = 0


# globals everyone can bitch about (that are actually just db objects in testing)
branch_url = 'https://github.com/NinjaBunny9000/DeepThonk/tree/raid-game' # TODO move to db
repo_url = 'https://github.com/NinjaBunny9000/DeepThonk/'


@twitch_bot.command('branch', alias=['current'])
async def branch(message):
    token = tokenize(message, 1)
    global branch_url
    
    if is_mod(message) and len(token) == 2:
        # !branch <url> ==> token[0] token[1]
        branch_url = token[1]
        msg = 'New branch set to \"{}\"'.format(branch_url)
        await twitch_bot.say(message.channel, msg)
    else:
        msg = "The branch Bun's working in rn is: {}".format(branch_url)
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('repo', alias=['repository', 'suppository'])
async def repo(message):
    token = tokenize(message, 1)
    global repo_url
    
    if is_mod(message) and len(token) == 2:
        # !repo <url> ==> token[0] token[1]
        repo_url = token[1]
        msg = 'New project repo set to \"{}\"'.format(repo_url)
        await twitch_bot.say(message.channel, msg)
    else:
        msg = "The repo Bun's working with rn is: {}".format(repo_url)
        await twitch_bot.say(message.channel, msg)
