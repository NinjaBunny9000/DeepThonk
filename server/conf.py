""" Imports settings & secrets (for integrations)
"""

import os
import sys
import logging

log = logging.getLogger('deepthonk')
log.debug(f"{__name__} loaded")

# Verify the .env file has been configured
if all(var in os.environ for var in (
        "SECRET_KEY"
        )):
    pass
else:
    print("You need to add your secrets to the .env-example file. Be sure to rename to \".env\".")

secret_key = os.environ['SECRET_KEY']