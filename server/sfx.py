"""Checks filesystem for audio files that the bot app turns into SFX commands."""

import os
from utils.logger import loggymclogger as log

list_of_sfx_files = []
sfx_with_extentions = []

path = 'static/sfx/hooks/'
for file in os.listdir(path):
    # create instance with attributes
    if file.endswith('.ogg') or file.endswith('.mp3'):
        
        # add the file name to a list (including the extension)
        sfx_with_extentions.append(file)
        file = file[:-4]  # removes the sextension
        list_of_sfx_files.append(file)

log.debug(f"SFX Loaded: {list_of_sfx_files}")
