import requests
import json

import data_tools

"""
!poll add <poll title goes here>
deepthonk: @<mod> Poll initiated. Awaiting options...
!poll 1 <option 1 goes here>
!poll 2 <option 2 goes here>
!poll 3 <option 3 goes here>
deepthonk: <poll preview>
!poll <accept/cancel>
deepthonk: Here's a link to the poll: <url>
"""

poll_endpoint = 'https://www.strawpoll.me/api/v2/polls'
poll_id = 0
straw_poll = {
    'title' : '',
    'options' : []
}

def set_name(name):
    global straw_poll
    straw_poll['title'] = name

def add_option(option):
    global straw_poll
    straw_poll["options"].append(option)

def review_poll():
    options = data_tools.stringify_list(straw_poll['options'])
    # FIXME Make the formatting include the index/enum #
    jsonified_rollypolly = json.dumps(straw_poll, indent=2)
    print(jsonified_rollypolly)
    return f"title: {straw_poll['title']} // options: {options}"

def setup_poll():
    # json object with relevant body data
    jsonified_rollypolly = json.dumps(straw_poll, indent=2)
    # post request
    header = {'Content-Type' : 'application/json'}
    r = requests.post(poll_endpoint, data=jsonified_rollypolly, headers=header)
    # return object & parse
    r = r.json()
    # report returned url/poll-id
    print(r)
    global poll_id
    global poll_link
    poll_link = f"https://www.strawpoll.me/{r['id']}"
    return poll_link

def get_link():
    return poll_link

def get_winner():
    r = requests.get(f"{poll_endpoint}/{poll_id}")
    r = r.json()
    scores = r['scores']
    options = r['options']
    results = dict(zip(scores, options)) 
    winner = results[max(list(results.keys()))]
    return winner


