import requests
from conf import streamelements_id, streamelements_auth


def get_chatters():
    r = requests.get('https://tmi.twitch.tv/group/user/ninjabunny9000/chatters')
    r = r.json()
    chatters = r['chatters']['viewers']
    chatters.extend(r['chatters']['moderators'])
    chatters.extend(r['chatters']['staff'])
    chatters.extend(r['chatters']['admins'])
    chatters.extend(r['chatters']['vips'])

    for member in chatters:
        member.lower()

    return chatters


def get_points(user_name):
    r = requests.get(f'https://api.streamelements.com/kappa/v2/points/{streamelements_id}/{user_name.lower()}')
    r = r.json()
    return r['points']


def put_points(user_name, amount):
    headers = { 'Authorization' : streamelements_auth }
    r = requests.put(
        f'https://api.streamelements.com/kappa/v2/points/{streamelements_id}/{user_name.lower()}/{amount}', 
        headers=headers
    )
    r = r.json()
    print(r)