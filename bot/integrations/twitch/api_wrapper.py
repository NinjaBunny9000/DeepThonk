import requests
from config.importer import bot, twitch_client_id, twitch_channel, twitch_team
from utils.logger import loggymclogger as log

log.debug(f"{__name__} loaded")

class Interface():

    # TODO use @property and @x.getter tags

    def __init__(self, base, accept, streamer, client_id):
        self.base = base
        self.streamer = streamer
        self.header = {
            'Accept' : accept,
            'Client-ID' : client_id
        }
        self.channel_id = self._get_channel_id()
        self.team_members = self._get_team_members()
        self.broadcasting = self._get_channel_status()
        self.game_rank = self._get_game_rank()

    def request(self, method, url, params=None, limit=None, version='kraken'):
        if method is 'GET':
            r = requests.get(f"{self.base}/{version}/{url}", headers=self.header)
            return r.json()

    def _get_team_members(self):
        data = self.request('GET', f"teams/{twitch_team}")
        members = list()
        for user in data['users']:
            members.append(user['name'])
        return members

    def _get_channel_id(self):
        data = self.request('GET', f"users?login={twitch_channel}")
        return data['users'][0]['_id']

    def _get_channel_status(self):
        data = self.request('GET', f"streams/{self.channel_id}")
        if data['stream'] is None:
            return False
        else:
            return True

    def _get_game_rank(self):
        # request data from api
        listyboi = list()
        data = self.request('GET', f"streams?game_id=509670", version='helix') # TODO pull game/category
        for stream in data['data']:
            # print(stream['user_name'])
            listyboi.append(stream['user_name'].lower())

        return listyboi

        # iterate through data and make list of channels
        # compare rank?

    def monitor_broadcast_state(self):
        self.broadcasting = self._get_channel_status()
        # track if stream started or stopped
        # mark if new stream or nah


base = "https://api.twitch.tv"
accept = "application/vnd.twitchtv.v5+json"

interface = Interface(base, accept, twitch_channel, twitch_client_id)