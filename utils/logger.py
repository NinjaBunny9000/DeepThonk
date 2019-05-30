import logging

# create logger object
loggyballs = logging.getLogger()
loggyballs.setLevel(logging.DEBUG)

# create file handler
fh = logging.FileHandler('error_log.txt')
fh.setLevel(logging.WARNING)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# format
fh_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
ch_formatter = logging.Formatter('[%(levelname)s] %(message)s')
fh.setFormatter(fh_formatter)
ch.setFormatter(ch_formatter)

# add/register them with the logger obj
loggyballs.addHandler(fh)
loggyballs.addHandler(ch)

loggyballs.info('I\'m back baby!')
