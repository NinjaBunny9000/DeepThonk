import requests
from conf import streamelements_id, streamelements_auth


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