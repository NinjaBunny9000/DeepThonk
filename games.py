from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin, bot_name
import asyncio
from obs_ctrl import change_scene, get_scene
from permissions import is_bot, is_mod
import time
import random
import api_integrations
from sfx import play_sfx
import data_tools
from cah import play_hand
import os


# config ze bot!
twitch_bot = twitch_instance


###############################################################################
# SECTION Earworm Roulet™
###############################################################################

@twitch_bot.command('earworm')
async def earworm(message):

# TODO 
# - Report what they won or not
# - Send a link to the youtube song, cuz you know they'll need it. Also it's polite.
# - Timeouts
# - Betting in general
# - Integrate StreamElements points
# - Help command/function

	# SECTION They win
	if random.random() >= 0.9:
		msg = 'u lucked tf out, @{}.'.format(message.author.name)
		await twitch_bot.say(message.channel, msg)
		return

	# !SECTION 


	# SECTION They lose
	msg = 'rip, @{}'.format(message.author.name)
	await twitch_bot.say(message.channel, msg)
	
	files = []

	# create a list of mp3s in folders (excluding aliases.txt)
	for file_name in os.listdir('sfx/earworms/'):
		if not file_name.endswith('.txt'):
			# add it to a list
			files.append(file_name)

	random_mp3 = 'sfx/earworms/{}'.format(random.choice(files))

	# playsound(random_mp3)
	play_sfx(random_mp3)

	# !SECTION     

# !SECTION 

###############################################################################
# SECTION Raid Game
###############################################################################

# globals everyone can bitch about (that are actually just db objects in testing)
emote_count = 0
emotes_this_raid = 0
attacker_score = 0
defender_score = 0
raid_status = False
raid_defender_members = []
raid_attacker_members = []
raid_in_progress = False
current_defenders = []
current_raiders = []

raiding = None
defending = None


# ANCHOR Classes / Teams

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
        self.hp = 500
        self.emotes = 0
        # healing vs attacking emotes?
        # emote dmg/weight??


class RaidAttackers:
    'Everyone that entered the channel after the raid started.'

    def __init__(self, attackers):
        self.id = 'RAIDERS' # TODO change later to be raiding channel
        self.members = attackers
        self.hp = 500
        self.emotes = 0
        # healing vs attacking emotes?
        # emote dmg/weight??


 
def raid_is_happening():
    global raid_status
    return raid_status


def count_emotes(message):
    global emote_count
    emote_count += len(message.emotes)
    return emote_count


#trigger teh start of a raid
def raid_start():
    global raid_in_progress
    if raid_in_progress == True:
        return True

# REVIEW why was this needed? still needed?
def raid_event(message):
    success_msg = "raid triggered successfully"
    print(success_msg)
    # lock all other reacts
    # say who's raiding & with how many pplz
    # say who won last raid
    # start counting emotes


def emotes_spammed():
    global emotes_this_raid
    return emotes_this_raid


def keep_score(message):
    global attacker_score
    global defender_score
    global raid_attacker_members
    global raid_defender_members

    if message.author.name.lower() in raid_attacker_members:
        attacker_score += len(message.emotes)
        
    if message.author.name.lower() in raid_defender_members:
        defender_score += len(message.emotes)

def keep_oop_score(message):
    global attacker_score
    global defender_score
    global raiding
    global defending

    if message.author.name.lower() in raiding.members:
        attacker_score += len(message.emotes)
        
    if message.author.name.lower() in defending.members:
        defender_score += len(message.emotes)


def get_def_count():
    global raid_defender_members
    return len(raid_defender_members)

def deal_damage(message):
    global attacker_score
    global defender_score
    global raiding
    global defending

    if message.author.name.lower() in raiding.members:
        defending.hp -= len(message.emotes)
        
    if message.author.name.lower() in defending.members:
        raiding.hp -= len(message.emotes)


def split_chatters(chatters):
    # random.shuffle(chatters)
    # index = len(chatters)//2
    # return chatters[:index]
    return random.sample(chatters, len(chatters)//2)


def who_raided():
    """
    Returns a list of who just raided. For now, this randomly splits the current
    members of the room between attackers & defenders.

    Eventually, this will be a difference of who was in the room before the raid,
    and who was in the room after the raid webhook dropped.
    """
    global raid_defender_members
    global raid_attacker_members 

    # DEBUG: shuffle the list & split the chatters in two
    attackers = split_chatters(raid_defender_members) # returns half of a shuffled list
    
    # take a diff of the list (attackers)
    for member in attackers:
        raid_defender_members.remove(member)

    return attackers


def assign_teams(): 
    'Determines attackers & defenders for the raid'

    global raid_attacker_members
    global raid_defender_members
  
    raid_defender_members = current_defenders   
    raid_attacker_members = who_raided() # DEBUG


def assign_test_teams(): 
    'Determines attackers & defenders for the raid'

    global raid_attacker_members
    global raid_defender_members
  
    raid_defender_members = api_integrations.get_chatters()    # TODO: eventually this will happen periodically
    raid_attacker_members = who_raided() # DEBUG


def create_oop_teams(): 
    'Creates instances of attackers & defenders.'

    global raid_attacker_members    # debug
    global raid_defender_members    # debug

    # create lists of attackers and defenders & make dem instances n wotnot
    global defending
    global raiding
    defending = RaidDefenders(raid_defender_members)
    raiding = RaidAttackers(raid_attacker_members)



def create_oop_test_teams(): 
    'Creates instances of attackers & defenders.'

    assign_test_teams()  # debug
    global raid_attacker_members    # debug
    global raid_defender_members    # debug

    # create lists of attackers and defenders & make dem instances n wotnot
    global defending
    global raiding
    defending = RaidDefenders(raid_defender_members)
    raiding = RaidAttackers(raid_attacker_members)

# def keep_score(message):
    # global emotes_this_raid
    # emotes_this_raid += len(message.emotes)


def reset_emote_count():
    global emote_count
    emote_count = 0


def reset_raid_score():
    global attacker_score
    global defender_score
    global raid_attacker_members
    global raid_defender_members

    attacker_score = 0
    defender_score = 0
    raid_attacker_members[:] = []
    raid_defender_members[:] = []

# def reset_raid_score():
#     global emotes_this_raid
#     emotes_this_raid = 0

# debug
def get_attacker_score():
    return attacker_score

# debug
def get_defender_score():
    return defender_score
        

def update_defenders_list():
    global raid_defender_members
    raid_defender_members = api_integrations.get_chatters()


def append_defenders(user):
    raid_defender_members.append(user.name)


def append_raiders(user):
    # if raid is scoring, it'll need to append to the raid instance
    if raid_status:
        raiding.members.append(user.name)
    else: # if raid hasn't started scoring
        raid_attacker_members.append(user.name)
        print('[RAIDER] @{} registered.'.format(user.name)) # TODO Logging


# debug
def print_teams(
    raiders=raid_attacker_members, 
    defenders=raid_defender_members
    ):
    # report list of memebrs to console
    # make the lits legible
    attackers_printable = raiders
    attackers_printable = '[%s]' % ', '.join(map(str, attackers_printable))
    attackers_printable = attackers_printable.strip('[]')
    defenders_printable = defenders
    defenders_printable = '[%s]' % ', '.join(map(str, defenders_printable))
    defenders_printable = defenders_printable.strip('[]')

    # print out who we gots
    print('\n[A RAID HAS BEGUN]\n') # TODO Logging


def report_ko():
    global raiding
    global defending

    if raiding.hp <= 0 or defending.hp <= 0:
        return True
    else:
        return False

def end_raid():
    global raid_status
    raid_status = False


def reset_raid():
    print('resetting raid score') # TODO Logging???
    data_tools.clear_txt('data/', 'raid_score.txt')

def get_winner():
    global raiding
    global defending

    if raiding.hp <= 0:
        return defending.id
    elif defending.hp <= 0:
        return raiding.id

def hp_condition():
    global raiding
    global defending

    # checks if hp is worth reporting
    if raiding.hp <= 50:
        return raiding.id
    elif defending.hp <= 50:
        return defending.id
    else:
        return False
   
def report_hp():
    # if hp is worth reporting, report it.
    if hp_condition():
        return hp_condition()

# SECTION Raid Game



@twitch_bot.command('raid')
async def raid(message):
    
    if message.author.name == "streamelements" or message.author.name.lower() == "ninjabunny9000":
        
        # start teh raid sequcence
        global raid_in_progress
        raid_in_progress = False # FIXME why does this need to be here?
        play_sfx('sfx/events/raid.mp3')
        raid_in_progress = True

        # !globals (pls dont cry)
        global raid_status
        global raiding
        global defending

        # also pls dont dubble-rade
        if raid_status:
            return

        # oop test
        create_oop_teams()
        print_teams(raiding.members, defending.members)

        # flip the bool bit thing so on_message can process emotes
        raid_status = True

        await twitch_bot.say(message.channel, "!redalert")  # RED LIGHTS

        await asyncio.sleep(7)  # 9s BSOD
        change_scene('BSOD')
        
        await asyncio.sleep(14)  # 15s
        msg = 'ATTENTION, NINJAS! We\'ve been RAIDED! Our networks are vulnerable!!'
        await twitch_bot.say(message.channel, msg)

        # report hp
        msg = """Raiders & Defenders both start with 100 hp. Spam emotes to deal damage!
         First team to drop to 0 hp loses teh raid!
        """
        await twitch_bot.say(message.channel, msg)
        
        await asyncio.sleep(10)  # 25s Switch to HackerTyper
        change_scene('RAID')

        # flip the bool bit thing so on_message can process emotes
        raid_status = True
        
        msg = 'Type defendNetwork(); to harness avilable blockchains. Boost our firewall\'s signal with any and all available shit-tier memes.'
        await twitch_bot.say(message.channel, msg)
       
       
@twitch_bot.command('raidover')
async def raidover(message):
    global emotes_this_raid
    global raid_in_progress

    # Let sfx be interruptable again 
    raid_in_progress = False    # REVIEW this could be handled better

    play_sfx('sfx/randoms/disabled/disabled.mp3')
    change_scene('RAID2')
    await twitch_bot.say(message.channel, "Keepo")
    await asyncio.sleep(1)
    change_scene('MAIN')

    # report the score
    msg = '!airhorn RAID OVER!. {} emotes were spammeded. Final Score was Attackers: {}, Defenders: {}'.format(
        (100-raiding.hp) + (100-defending.hp), raiding.hp, defending.hp
        )
    await twitch_bot.say(message.channel, msg) 

    reset_raid()
    reset_raid_score()

# !SECTION   

# ─── DEBUG COMMANDS ─────────────────────────────────────────────────────────────


@twitch_bot.command('debugreacts')
async def debugreacts(message):
    """
    DEBUG: change msg var to print whatever var u tryin'a lern gooder
    """
    msg = bot_name().lower()   
    await twitch_bot.say(message.channel, msg)


# counts the emotes in a message ==> !emote <emotes>
@twitch_bot.command('emote')
async def emote(message):
    count = 0
    for emote in message.emotes:
        count = count + 1
    await twitch_bot.say(message.channel, str(count)) 


@twitch_bot.command('testraid')
async def testraid(message):
    'Tests raid function'

    """
    TODO GET RAIDS WORKING AGAIN!SECTION 
     - [ ] Raid timer stuffs?
     - [ ] Actually split up the room between actaul raiders and actual defenders
    """

    if message.author.name == "streamelements" or message.author.name.lower() == "ninjabunny9000":
        
        # start teh raid sequcence
        global raid_in_progress
        raid_in_progress = False # FIXME why does this need to be here?
        play_sfx('sfx/events/raid.mp3')
        raid_in_progress = True

        # !globals (pls dont cry)
        global raid_status
        global raiding
        global defending

        # also pls dont dubble-rade
        if raid_status:
            return

        # oop test
        create_oop_test_teams()
        print_teams(raiding.members, defending.members)

        # flip the bool bit thing so on_message can process emotes
        raid_status = True

        await twitch_bot.say(message.channel, "!redalert")  # RED LIGHTS

        await asyncio.sleep(7)  # 9s BSOD
        change_scene('BSOD')
        
        await asyncio.sleep(14)  # 15s
        msg = 'ATTENTION, NINJAS! We\'ve been RAIDED! Our networks are vulnerable!!'
        await twitch_bot.say(message.channel, msg)

        # report hp
        msg = """Raiders & Defenders both start with 100 hp. Spam emotes to deal damage!
         First team to drop to 0 hp loses teh raid!
        """
        await twitch_bot.say(message.channel, msg)
        
        await asyncio.sleep(10)  # 25s Switch to HackerTyper
        change_scene('RAID')

        # flip the bool bit thing so on_message can process emotes
        raid_status = True
        
        msg = 'Type defendNetwork(); to harness avilable blockchains. Boost our firewall\'s signal with any and all available shit-tier memes.'
        await twitch_bot.say(message.channel, msg)

        


# REVIEW old raid test func?
# @twitch_bot.command('testraid')
# async def testraid(message):
#     global raid_status

#     # oop test
#     create_oop_teams()  
#     print_teams(raiding.members, defending.members)

#     # flip the bool bit thing so on_message can process emotes
#     raid_status = True

#     msg = 'raid in progress. spam a few emotes for teh test! kthx <3'
#     await twitch_bot.say(message.channel, msg)


@twitch_bot.command('endraidtest')
async def endraidtest(message):
    global raid_status
    global emotes_this_raid

    # flip the bool bit thing again
    raid_status = False

    # report the score
    msg = '!airhorn RAID OVER!. {} emotes were spammeded. Attackers: {}, Defenders: {}'.format(
        (100-raiding.hp) + (100-defending.hp), raiding.hp, defending.hp
        )
    await twitch_bot.say(message.channel, msg) 

    reset_raid()
    reset_raid_score()


@twitch_bot.command('raidstate')
async def raidstate(message):
    # flip the bool bit thing
    global raid_status
    if raid_status:
        msg = 'raid in progress.'
        await twitch_bot.say(message.channel, msg)
    else:
        msg = 'not in a raid rn'
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('setupraid')
async def setupraid(message):
    
    # assign OOP teams/instances & print to console for debugging
    create_oop_teams()

    global raiding
    global defending

    # print 'em out in console
    print_teams(raiding.members, defending.members)


# gets the current list of ppl in the chat room from twitch TMI
@twitch_bot.command('getchatters')
async def getchatters(message):
    print(api_integrations.get_chatters())


@twitch_bot.command('defenders')
async def defenders(message):
    msg = '{} defenders registered'.format(len(raid_defender_members))
    await twitch_bot.say(message.channel, msg)



# command registers that it needs to start counting emotes
    # do the bool thing

# count emotes every message
    """
    This is going to have to happen in a "on message" (twitch_chat.py) and somehow have
    access to the bool in *this* script. 0_o
    """

# command that stops counting 
    # report & of emotes during period


@twitch_bot.command('cah')
async def cah(message):
    """
    Cards against humanity play-generator.
    """
    await twitch_bot.say(message.channel, play_hand())


# SECTION Have You Ever