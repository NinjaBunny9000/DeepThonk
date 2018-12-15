from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin, bot_name
import asyncio
from obs_ctrl import change_scene, get_scene
from twitch_permissions import is_bot, is_mod
import time
import random
import api_integrations


# config ze bot!
twitch_bot = twitch_instance

# global vars
emote_count = 0
emotes_this_raid = 0
attacker_score = 0
defender_score = 0
raid_status = False
raid_defender_members = []
raid_attacker_members = []

raiding = None
defending = None


# ─── CLASSES ────────────────────────────────────────────────────────────────────

# defenders = RaidDefenders(current_members)
# attackers = RaidAttackers(raid_members)
# new_raid = Raid(current_members, raid_members)

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
        self.hp = 100
        self.emotes = 0
        # healing vs attacking emotes?
        # emote dmg/weight??


class RaidAttackers:
    'Everyone that entered the channel after the raid started.'

    def __init__(self, attackers):
        self.id = 'RAIDERS' # TODO change later to be raiding channel
        self.members = attackers
        self.hp = 100
        self.emotes = 0
        # healing vs attacking emotes?
        # emote dmg/weight??


# ─── RAID SEQUENCE ──────────────────────────────────────────────────────────────
 
def raid_is_happening():
    global raid_status
    return raid_status

def count_emotes(message):
    global emote_count
    emote_count += len(message.emotes)
    return emote_count


#trigger teh start of a raid
def raid_start(message):
    # chk the message or webhooks for raid triggers
    if "trigger raid" in message.content.lower():
        return True


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
  
    raid_defender_members = api_integrations.get_chatters()    # TODO: eventually this will happen periodically
    raid_attacker_members = who_raided() # DEBUG


def create_oop_teams(): 
    'Creates instances of attackers & defenders.'

    assign_teams()  # debug
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
    print('attackers: {} \n'.format(attackers_printable))
    print('defenders: {}'.format(defenders_printable))

def report_ko():
    global raiding
    global defending

    if raiding.hp <= 0 or defending.hp <= 0:
        print('[RETURNED TRUE]')
        return True
    else:
        return False

def end_raid():
    global raid_status
    raid_status = False

def get_winner():
    global raiding
    global defending

    if raiding.hp <= 0:
        return defending.id
    elif defending.hp <= 0:
        return raiding.id

#start counting emotes & keep score

#report score (emote count)



@twitch_bot.command('raid')
async def raid(message):
    if is_mod(message) or message.author.name == "streamelements":
        await asyncio.sleep(4)
        await twitch_bot.say(message.channel, "!redalert")  # RED LIGHTS

        await asyncio.sleep(5)  # 9s BSOD
        change_scene('BSOD')
        
        await asyncio.sleep(6)  # 15s
        msg = 'ATTENTION, NINJAS! We\'ve been RAIDED! Our networks are vulnerable!!'
        await twitch_bot.say(message.channel, msg)
        
        await asyncio.sleep(10)  # 25s Switch to HackerTyper
        change_scene('RAID')
        
        await asyncio.sleep(4) 
        msg = 'Type defendNetwork(); to harness avilable blockchains and boost our firewall\'s signal.'
        await twitch_bot.say(message.channel, msg)

        await asyncio.sleep(10) 
        msg = 'Network defenses are failing. Initiate all protocols! Pizza! Donuts! Bacon!! THROW ALL WE\'VE GOT AT THEM!!'
        await twitch_bot.say(message.channel, msg)

        await asyncio.sleep(5) # 40s Pizza
        await twitch_bot.say(message.channel, "pizzaProtocol();")

                
@twitch_bot.command('raidover')
async def raidover(message):
    if is_mod(message):
        msg = "!disabled3"
        await twitch_bot.say(message.channel, msg)
        change_scene('RAID2')
        await twitch_bot.say(message.channel, "Keepo")
        await asyncio.sleep(2) #
        change_scene('MAIN')

   

# ─── DEBUG COMMANDS ─────────────────────────────────────────────────────────────

@twitch_bot.command('debugreacts')
async def debugreacts(message):
    """
    DEBUG: change msg var to print whatever var u tryin'a lern gooder
    """
    msg = bot_name().lower()   
    await twitch_bot.say(message.channel, msg)

def raid_in_progress(message):
    # chk the message or webhooks for raid triggers
    if "trigger raid" in message.content.lower():
        print("raid in progress")
        return True

# switch scene to GAMES    
@twitch_bot.command('emote')
async def emote(message):
    # print(message.content.emotes)
    print(message.emotes)
    count = 0
    for emote in message.emotes:
        count = count + 1
    await twitch_bot.say(message.channel, str(count)) 
    # except:
    #     msg = "no emotes"
    #     await twitch_bot.say(message.channel, msg) 


@twitch_bot.command('testraid')
async def testraid(message):
    global raid_status

    # assign_teams()
    # print_teams()

    # oop test
    create_oop_teams()  
    print_teams(raiding.members, defending.members)

    # flip the bool bit thing so on_message can process emotes
    raid_status = True

    msg = 'raid in progress. spam a few emotes for teh test! kthx <3'
    await twitch_bot.say(message.channel, msg)


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







# @twitch_bot.command('endraidtest')
# async def endraidtest(message):
#     # flip the bool bit thing again
#     global raid_status
#     global emotes_this_raid
#     raid_status = False
#     # spit out the count of emotes that were dropped during the raid
#     msg = 'raid ended. {} emotes were spammeded.'.format(emotes_this_raid)
#     await twitch_bot.say(message.channel, msg) 
#     msg = 'state={}'.format(raid_status)
#     await twitch_bot.say(message.channel, msg) 
#     reset_raid_score()


# command registers that it needs to start counting emotes
    # do the bool thing

# count emotes every message
    """
    This is going to have to happen in a "on message" (twitch_chat.py) and somehow have
    access to the bool in *this* script. 0_o
    """

# command that stops counting 
    # report & of emotes during period