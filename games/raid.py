import asyncio
import time
import random

# internal modules & packages
import conf
import data_tools
import integrations.twitch.api_wrapper
from integrations.obs.ctrl import change_scene, get_scene
from integrations.twitch.privilege import is_bot, is_mod
from sfx.sfx import play_sfx

# config ze bot!
twitch_bot = conf.twitch_instance

# TODO Logging - ___ module loaded


###############################################################################
# SECTION Raid Game
###############################################################################

# globals everyone can bitch about (that are actually just db objects in testing)
emote_count = 0
raid_in_progress = False
raid_defender_members = []
raid_attacker_members = []
raid_started = False
current_defenders = []
current_raiders = []

raiding = None
defending = None


# ANCHOR Classes / Teams
###############################################################################

class Raid:
    'Keeps track of the status and history of raids'

    raiders = {}

    def __init__(self, raiders, defenders):
        self.status = True
        self.time = time.time() # TODO format this better kthx
        self.raiders = raiders
        self.defenders = defenders


class RaidDefenders:
    'Everyone that was in the channel before the raid started.'

    def __init__(self, defenders):
        self.id = 'DEFENDERS' # debug
        self.members = defenders
        self.hp = conf.raid['max_hp']
        self.emotes = 0


class RaidAttackers:
    'Everyone that entered the channel & sent a msg after the raid started.'

    def __init__(self, attackers):
        self.id = 'RAIDERS' # TODO change later to be raiding channel
        self.members = attackers
        self.hp = conf.raid['max_hp']
        self.emotes = 0


# ANCHOR Functions
###############################################################################

def is_happening():
    global raid_in_progress
    return raid_in_progress


#trigger teh start of a raid
def start():
    global raid_started
    if raid_started == True:
        return True
    else:
        return False


def deal_damage(message):
    global raiding
    global defending

    if message.author.name.lower() in raiding.members:
        defending.hp -= len(message.emotes)*2.5
        
    if message.author.name.lower() in defending.members:
        raiding.hp -= len(message.emotes)


def create_teams(): 
    'Creates instances of attackers & defenders objects.'

    # create lists of attackers and defenders & make dem instances n wotnot
    global defending
    global raiding

    defending = RaidDefenders(raid_defender_members)
    raiding = RaidAttackers(raid_attacker_members)


def reset_score():
    global raid_attacker_members
    global raid_defender_members
    raid_attacker_members[:] = []
    raid_defender_members[:] = []
    # reset list of people in the room to all be defenders
    update_defenders_list()


def update_defenders_list():
    global raid_defender_members
    raid_defender_members = integrations.twitch.api_wrapper.get_chatters()


def append_defenders(chatter):
    # check if they're in the defender list already
    if chatter not in raid_defender_members and chatter not in raid_attacker_members:
        # add them if they aren't
        raid_defender_members.append(chatter)
        # print(f'[DEFENDER] {chatter} registered.')


# FIXME compares list to instance attribute
# TODO make another function that compares list to instance attribute and adds
# ppl not on it
def append_raiders(message):
    # define teh chatter
    chatter = message.author.name
    # check if they're in the defender list already
    if chatter not in raid_defender_members and chatter not in raid_attacker_members:
        # add them if they aren't
        raid_attacker_members.append(chatter)
        raiding.members.append(chatter)
        # report/debug to serail
        print(f'[RAIDER] {chatter} registered.')


def report_ko():
    if raiding.hp <= 0 or defending.hp <= 0:
        return True
    else:
        return False


def stop():
    global raid_in_progress
    raid_in_progress = False


def reset_raid():
    print('resetting raid score') # TODO Logging???
    # data_tools.clear_txt('data/', 'raid_score.txt')
    data_tools.score_to_txt(conf.raid['max_hp'], conf.raid['max_hp'])


def get_winner():
    if raiding.hp <= 0:
        return defending.id
    elif defending.hp <= 0:
        return raiding.id


def get_team(message):
    chatter = message.author.name
    teams = list()
    if chatter in raid_defender_members:
        # append report
        teams.append('defenders')
    if chatter in raid_attacker_members:
        # append report
        teams.append('attackers')
    if chatter not in raid_defender_members and chatter not in raid_attacker_members:
        # not in any team... wtf!?
        teams.append('none')

    return data_tools.stringify_list(teams)  # send report


# REVIEW (kind of a debug function)
def swap_teams(chatter):
    global raid_attacker_members
    global raid_defender_members

    chatter = chatter.lower()

    if chatter in raid_defender_members:
        # remove from defenders
        raid_defender_members.remove(chatter)
        # add to attackers
        raid_attacker_members.append(chatter)
    elif chatter in raid_attacker_members:
        # remove from attacekrs
        raid_attacker_members.remove(chatter)
        # add to defenders
        raid_defender_members.append(chatter)
    else:
        # make sure they're at least on teh raiding team
        raid_attacker_members.append(chatter)


def swap_raider(raider):
    global raid_attacker_members
    global raid_defender_members

    raider = raider.lower()

    if raider in raid_defender_members:
        # remove from defenders
        raid_defender_members.remove(raider)
        # add to attackers
        raid_attacker_members.append(raider)
    else:
        # make sure they're at least on teh raiding team
        raid_attacker_members.append(raider)


def get_raiders():
    return data_tools.stringify_list(raid_attacker_members)


def get_defenders():
    return data_tools.stringify_list(raid_defender_members)


# ANCHOR  Raid Function
###############################################################################

@twitch_bot.command('raid')
async def raid(message):

    if message.author.name.lower() in conf.bot_list:
        pass
    else:
        print(f'no permissions for raid!!')
        return

    # start teh raid sequcence
    global raid_started
    raid_started = False # FIXME why does this need to be here?
    play_sfx('sfx/events/raid.mp3')

    # REVIEW NinjaBunny9000 channel only!
    if conf.twitch_channel.lower() == 'ninjabunny9000'.lower():
        await twitch_bot.say(message.channel, "!redalert")  # RED LIGHTS

    raid_started = True

    # !globals (pls dont cry)
    global raid_in_progress

    # also pls dont dubble-rade
    if raid_in_progress:
        return

    # parse tokens from SE bot command to get the raider name
    token = data_tools.tokenize(message, 2)
    raider_name = data_tools.ats_or_nah(token[1])

    # add the raider to the correct team
    swap_raider(raider_name)

    create_teams()

    await asyncio.sleep(conf.raid['raid_delay'])

    # display the game rules, if enabled
    if conf.raid['custom_rules_scene']:
        change_scene(conf.raid['rules_scene'])
        await asyncio.sleep(conf.raid['rules_timer'])

    msg = '🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨'
    await twitch_bot.say(message.channel, msg)
    msg = '🚨 ATTENTION!!! 🚨 We\'ve been RAIDED! Our networks are vulnerable!!'
    await twitch_bot.say(message.channel, msg)

    # report hp
    max_hp = conf.raid['max_hp']
    msg = f'Raiders & Defenders both start with {max_hp} hp. First team to drop to 0 hp loses teh raid!'
    await twitch_bot.say(message.channel, msg)
    msg = 'Spam emotes to deal damage!'
    await twitch_bot.say(message.channel, msg)

    # flip the bool bit thing so on_message can process emotes
    raid_in_progress = True

    # custom raid scene
    if conf.raid['custom_raid_scene']:
        await asyncio.sleep(conf.raid['raid_delay'])  
        change_scene(conf.raid['raid_scene'])
    
    msg = 'Type defendNetwork(); to harness avilable blockchains. Boost our firewall\'s signal with any and all available emotes.'
    await twitch_bot.say(message.channel, msg)
    

@twitch_bot.command('raidover')
async def raidover(message):
    global raid_started
    global raid_in_progress

    # Let sfx be interruptable again 
    raid_started = False    # REVIEW this could be handled better
    raid_in_progress = False

    # REVIEW NinjaBunny9000 channel only!
    if conf.twitch_channel.lower() == 'ninjabunny9000'.lower():
        play_sfx('sfx/randoms/disabled/disabled.mp3')
    change_scene(conf.raid['victory_scene'])
    await twitch_bot.say(message.channel, "Keepo")
    await asyncio.sleep(1)
    change_scene(conf.scenes['main'])

    max_hp = conf.raid['max_hp']
    # report the score
    try:
        msg = f'!airhorn RAID OVER!. {(max_hp-raiding.hp) + (max_hp-defending.hp)} emotes were spammeded. Final Score was Attackers: {raiding.hp}, Defenders: {defending.hp}'
    except AttributeError:
        msg = 'wut raid? Kappa'
    await twitch_bot.say(message.channel, msg) 

    reset_raid()
    reset_score()

# !SECTION

# fakes a raid start
@twitch_bot.command('fakeraid')
async def fakeraid(message):
    
    print('command entered')

    if message.author.name.lower() == 'ninjabunny9000':
        pass
    else:
        print('command exited')
        return
    
    # start teh raid sequcence
    global raid_started
    raid_started = False # FIXME why does this need to be here?

    # REVIEW NinjaBunny9000 channel only!
    if conf.twitch_channel.lower() == 'ninjabunny9000'.lower():
        await twitch_bot.say(message.channel, "!redalert")  # RED LIGHTS

    raid_started = True

    # !globals (pls dont cry)
    global raid_in_progress

    # also pls dont dubble-rade
    if raid_in_progress:
        return

    create_teams()

    # display the game rules, if enabled
    msg = '🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨'
    await twitch_bot.say(message.channel, msg)

    # flip the bool bit thing so on_message can process emotes
    raid_in_progress = True