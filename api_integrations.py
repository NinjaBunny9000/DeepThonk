import requests

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

