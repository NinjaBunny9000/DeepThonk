from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
import os, random
from playsound import playsound 
from twitch_chat import stringify_list


# config ze bot!
twitch_bot = twitch_instance


###################################################################
# SECTION SFX Generation via folder/file structure bidness
###################################################################

class SoundEffect(object):
    """
    Base class for all sound effects.

    Eventually looks like ==> SoundEffect(file_name, permission_level, cost, cooldown).
    """

    commands = []

    # constructor
    def __init__(self, cmd_name, cmd_path):
        self.cmd = cmd_name
        self.path = cmd_path

        # TODO: Check and see if pre-existing command
        # create/register file as command in event-loop
        @twitch_bot.command(self.cmd)
        async def sfx_func(message):
            if message.author.subscriber:
                playsound(self.path)
        
        # add the command name to a list to be used later for spreadsheet generation
        SoundEffect.commands.append(cmd_name)


# REVIEW  move into a function later during refactor
# for every file in directory (os.listdir(path))
path = 'sfx/hooks/'
for file in os.listdir(path):

    # create instance with attributes
    if file.endswith('.mp3'):
        cmd_name = file[:-4]
        cmd_path = path + file
        debug_msg = 'cmd_name={} cmd_path={}'.format(cmd_name, cmd_path)
        SoundEffect(cmd_name, cmd_path)


# REVIEW function these out in a refactor
@twitch_bot.command('sfx')
async def sfx(message):
    """
    Spits out a list of SFX commands. Pretty simple at the moment.
    """

    # TODO https://github.com/NinjaBunny9000/DeepThonk/issues/26
    
    msg = 'SFX can be used freely by subscribers! :D '

    # for every item in an enumerated list of commands
    for cmd in SoundEffect.commands:
        cmd = '!{}'.format(cmd) # add the !

        # get the length of the string & compare it to teh length it would be if it added the new command
        if (len(msg) + len(cmd) + 2) >= 500:
            # send message and start over
            await twitch_bot.say(message.channel, msg)  # TODO Add page number
            msg = ''
        else:
            # add to msg
            if len(msg) is 0:
                msg += cmd
            else:
                msg += ', {}'.format(cmd)
    
    # then send the rest
    await twitch_bot.say(message.channel, msg) # TODO add final page number
            
 
###################################################################
# SECTION Randomized SFX
###################################################################

@twitch_bot.command('wow')
async def wow(message):
    random_mp3 = 'sfx/wow/' + random.choice(os.listdir('sfx/wow/'))
    playsound(random_mp3)


@twitch_bot.command('futurama')
async def futurama(message):
    random_mp3 = 'sfx/futurama/' + random.choice(os.listdir('sfx/futurama/'))
    playsound(random_mp3)


###################################################################
# SECTION Debug commands (remove in refactor, etc)
###################################################################
        
@twitch_bot.command('testwaifu')
async def testwaifu(message):
    playsound('sfx/hooks/waifu.mp3')