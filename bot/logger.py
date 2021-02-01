import logging

# create logger objectw
log = logging.getLogger('deepthonk')
log.setLevel(logging.DEBUG)

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
log.addHandler(fh)
log.addHandler(ch)
