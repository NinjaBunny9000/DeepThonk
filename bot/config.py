import os

class Config:
    def __init__(self):
        self.bot_nick = os.environ['TWITCH_BOT_NICK']
        self.token = os.getenv('TWITCH_TOKEN')
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.prefix = os.getenv('TWITCH_PREFIX')
        self.channel = os.getenv('TWITCH_CHANNEL')
        self.team = os.getenv('TWITCH_TEAM')


