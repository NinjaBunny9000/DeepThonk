import conf
from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin, bot_name
import asyncio
from obs_ctrl import change_scene, get_scene
from privilege import is_bot, is_mod
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
# SECTION Cards Against Humanity ™
###############################################################################

@twitch_bot.command('cah')
async def cah(message):
    'Cards against humanity play-generator.'

    await twitch_bot.say(message.channel, play_hand())

# !SECTION 


###############################################################################
# SECTION Earworm Roulet™ (WIP)
###############################################################################

@twitch_bot.command('earworm')
async def earworm(message):

    # TODO StreamElements Points Integration & Betting
    # - Integrate StreamElements points
    # - Report what they won or not
    # - Betting THE General™
    # - Help command/function

	# ANCHOR They win
	if random.random() >= 0.9:
		msg = f'u lucked tf out, @{message.author.name}.'
		await twitch_bot.say(message.channel, msg)
		return

	# ANCHOR They lose
	msg = f'rip, @{message.author.name}'
	await twitch_bot.say(message.channel, msg)

	files = []

	# create a list of mp3s in folders (excluding aliases.txt)
	for file_name in os.listdir('sfx/earworms/'):
		if not file_name.endswith('.txt'):
			files.append(file_name)

	random_mp3 = f'sfx/earworms/{random.choice(files)}'

	play_sfx(random_mp3)

# !SECTION 


###############################################################################
# SECTION Raid Game
###############################################################################

# globals everyone can bitch about (that are actually just db objects in testing)
emote_count = 0
raid_status = False
raid_defender_members = []
raid_attacker_members = []
raid_in_progress = False
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
        self.hp = 500
        self.emotes = 0


class RaidAttackers:
    'Everyone that entered the channel & sent a msg after the raid started.'

    def __init__(self, attackers):
        self.id = 'RAIDERS' # TODO change later to be raiding channel
        self.members = attackers
        self.hp = 500
        self.emotes = 0


# ANCHOR Functions
###############################################################################
 
def raid_is_happening():
    global raid_status
    return raid_status


#trigger teh start of a raid
def raid_start():
    global raid_in_progress
    if raid_in_progress == True:
        return True


def deal_damage(message):
    global raiding
    global defending

    if message.author.name.lower() in raiding.members:
        defending.hp -= len(message.emotes)
        
    if message.author.name.lower() in defending.members:
        raiding.hp -= len(message.emotes)


def create_teams(): 
    'Creates instances of attackers & defenders objects.'

    # create lists of attackers and defenders & make dem instances n wotnot
    global defending
    global raiding

    defending = RaidDefenders(raid_defender_members)
    raiding = RaidAttackers(raid_attacker_members)


def reset_raid_score():
    global raid_attacker_members
    global raid_defender_members
    raid_attacker_members[:] = []
    raid_defender_members[:] = []


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


def report_ko():
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
    if raiding.hp <= 0:
        return defending.id
    elif defending.hp <= 0:
        return raiding.id


# ANCHOR  Raid Function
###############################################################################

@twitch_bot.command('raid')
async def raid(message):
    
    for bot in conf.bot_list:
        if message.author.name.lower() != bot.lower():
            print('not bot')
            return

    if message.author.name.lower() == conf.streamer.lower():
        
        # start teh raid sequcence
        global raid_in_progress
        raid_in_progress = False # FIXME why does this need to be here?
        play_sfx('sfx/events/raid.mp3')

        # REVIEW NinjaBunny9000 channel only!
        if twitch_channel().lower() == 'ninjabunny9000'.lower():
            await twitch_bot.say(message.channel, "!redalert")  # RED LIGHTS

        raid_in_progress = True

        # !globals (pls dont cry)
        global raid_status

        # also pls dont dubble-rade
        if raid_status:
            return

        create_teams()

        # REVIEW NinjaBunny9000 channel only!
        if twitch_channel().lower() == 'ninjabunny9000'.lower():
            await asyncio.sleep(7)  # 9s BSOD
            change_scene('BSOD')
        
        await asyncio.sleep(14)  # 15s
        msg = '🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨'
        await twitch_bot.say(message.channel, msg)
        msg = '🚨 ATTENTION!!! 🚨 We\'ve been RAIDED! Our networks are vulnerable!!'
        await twitch_bot.say(message.channel, msg)

        # report hp
        msg = 'Raiders & Defenders both start with 500 hp. First team to drop to 0 hp loses teh raid!'
        await twitch_bot.say(message.channel, msg)
        msg = 'Spam emotes to deal damage!'
        await twitch_bot.say(message.channel, msg)

        # flip the bool bit thing so on_message can process emotes
        raid_status = True

        if conf.custom_settings['raid_scene']:
            await asyncio.sleep(conf.custom_settings['raid_timer'])  
            change_scene(conf.scenes['raid'])
        
        msg = 'Type defendNetwork(); to harness avilable blockchains. Boost our firewall\'s signal with any and all available emotes.'
        await twitch_bot.say(message.channel, msg)
       
       
@twitch_bot.command('raidover')
async def raidover(message):
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