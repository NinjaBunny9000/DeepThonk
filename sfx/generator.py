from conf import bot
from utils.logger import loggyballs as log

import os
import contextlib
with contextlib.redirect_stdout(None):
    from pygame import mixer

mixer.init(frequency=44100)

sfx_ch = 0

log.info(f"{__name__} imported!")


def play(full_file_path):
    mixer.Channel(sfx_ch).play(mixer.Sound(full_file_path))


class SoundEffect:
    'Generates teh functions for all the sfx comands'

    
    def __init__(self, cmd_name, cmd_path):
        'make an async func that registers/controls cmd'

        @bot.command(name=cmd_name)
        async def test_command(ctx):
            play(cmd_path)

        log.info(f"[SFX] !{cmd_name} registered!")


def generate_functions():
    path = 'sfx/hooks/'
    for file in os.listdir(path):
        if file.endswith('.ogg'):
            cmd_name = file[:-4]
            cmd_path = path + file
            SoundEffect(cmd_name, cmd_path)


generate_functions()