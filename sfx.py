from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
from pygame import mixer
import os, random
from playsound import playsound 


# config ze bot!
twitch_bot = twitch_instance

mixer.init()

class SoundEffect(object):
    """
    Base class for all sound effects. Eventually looks like ==> SoundEffect(file_name, permission_level, cost, cooldown).
    """

    # constructor
    def __init__(self, cmd_name, cmd_path):
        self.cmd = cmd_name
        self.path = cmd_path

        # TODO: Check and see if pre-existing command
        @twitch_bot.command(self.cmd)
        async def sfx_func(message):
            if message.author.subscriber:
                playsound(self.path)


# for every file in directory (os.listdir(path))
path = 'sfx/hooks/'
for file in os.listdir(path):

    # create instance with attributes
    if file.endswith('.mp3'):
        cmd_name = file[:-4]
        cmd_path = path + file
        debug_msg = 'cmd_name={} cmd_path={}'.format(cmd_name, cmd_path)
        SoundEffect(cmd_name, cmd_path)



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


# ─── SFX ────────────────────────────────────────────────────────────────────────

@twitch_bot.command('slideup')
async def slideup(message):
    mixer.music.load('sfx\\slideup.mp3')
    mixer.music.play()


@twitch_bot.command('wow')
async def wow(message):
    random_mp3 = 'sfx\\wow\\' + random.choice(os.listdir('C:\\Users\\spunk\\Documents\\repos\\BunBot9000\\sfx\\wow'))
    playsound(random_mp3)


@twitch_bot.command('futurama')
async def futurama(message):
    random_mp3 = 'sfx/futurama/' + random.choice(os.listdir('C:/Users/spunk/Documents/repos/BunBot9000/sfx/futurama/'))
    playsound(random_mp3)
