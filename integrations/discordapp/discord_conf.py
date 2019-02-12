import yaml
import os
import sys


# Load the integrations config file
with open(os.path.join(sys.path[0], 'secrets.yaml'), "r") as f:
    cfg = yaml.load(f)

token = cfg['discord']['token']
server_id = cfg['discord']['server_id']