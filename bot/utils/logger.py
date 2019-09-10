""" Master logger for the app

Import to use in any of the other apps with:
from utils.logger import loggymclogger as log

Then use like..

log.debug("log message")
"""

import logging

# create logger objectw
loggymclogger = logging.getLogger('deepthonk')
loggymclogger.setLevel(logging.DEBUG)

# create file handler
fh = logging.FileHandler('error_log.txt')
fh.setLevel(logging.WARNING)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# format
fh_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
ch_formatter = logging.Formatter('[%(levelname)s] %(message)s')
fh.setFormatter(fh_formatter)
ch.setFormatter(ch_formatter)

# add/register them with the logger obj
loggymclogger.addHandler(fh)
loggymclogger.addHandler(ch)
