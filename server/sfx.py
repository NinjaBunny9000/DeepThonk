"""Checks filesystem for audio files that the bot app turns into SFX commands."""

import os
from utils.logger import loggymclogger as log

list_of_sfx_files = []
sfx_with_extentions = []
rando_sfx_listyboi = []

path = 'static/sfx/hooks/'
for file in os.listdir(path):
    # create instance with attributes
    if file.endswith('.ogg') or file.endswith('.mp3') or file.endswith('.wav'):

        # add the file name to a list (including the extension)
        sfx_with_extentions.append(file)
        file = file[:-4]  # removes the sextension
        list_of_sfx_files.append(file)

log.debug(f"SFX Loaded: {list_of_sfx_files}")


# make a list of all the folders in 'static/sfx/random/'
rando_path = 'static/sfx/randos/'
for folder in os.listdir(rando_path):
    # add it all to a list
    log.debug(f"{folder} was detected as a random sfx command")
    rando_sfx_listyboi.append(folder)