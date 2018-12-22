from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
import os, random
from playsound import playsound 


# config ze bot!
twitch_bot = twitch_instance


class SoundEffect(object):
    """
    Base class for all sound effects. Eventually looks like ==> SoundEffect(file_name, permission_level, cost, cooldown).
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


# TODO move into a function later during refactor
# for every file in directory (os.listdir(path))
path = 'sfx/hooks/'
for file in os.listdir(path):

    # create instance with attributes
    if file.endswith('.mp3'):
        cmd_name = file[:-4]
        cmd_path = path + file
        debug_msg = 'cmd_name={} cmd_path={}'.format(cmd_name, cmd_path)
        SoundEffect(cmd_name, cmd_path)

# DEBUG : prints out a list of commands to make sure we have the syntax correct
print(SoundEffect.commands)



@twitch_bot.command('testsfx')
async def testsfx(message):

    # for every file in directory (os.listdir(path))
    path = 'sfx/hooks/'
    for file in os.listdir(path):

        # create instance with attributes
        if file.endswith('.mp3'):
            cmd_name = file[:-4]
            cmd_path = path + file
            debug_msg = 'cmd_name={} path={}'.format(cmd_name, cmd_path)
            print(debug_msg)
            # SoundEffect(cmd_name, path)

        
@twitch_bot.command('testwaifu')
async def testwaifu(message):
    playsound('sfx/hooks/waifu.mp3')


"""
RANDOMIZED SOUND EFFECTS
"""

@twitch_bot.command('wow')
async def wow(message):
    random_mp3 = 'sfx\\wow\\' + random.choice(os.listdir('C:\\Users\\spunk\\Documents\\repos\\BunBot9000\\sfx\\wow'))
    playsound(random_mp3)


@twitch_bot.command('futurama')
async def futurama(message):
    random_mp3 = 'sfx/futurama/' + random.choice(os.listdir('C:/Users/spunk/Documents/repos/BunBot9000/sfx/futurama/'))
    playsound(random_mp3)
