from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin
import os, random, time
import csv
from pygame import mixer
import games


# config ze bot!
twitch_bot = twitch_instance


mixer.init(frequency=44100)


def play_sfx(full_file_path, r00d=True, unr00dable=False):
	'Interrupts any sound being played and plays the new one that\'s passed in'
	# TODO additional argument for interruptability or nah

	# prevent trampling over raid routine
	if full_file_path == 'sfx/events/raid_victory.mp3':
		pass
	elif games.raid_start():
		print('SFX ABORTED')
		return

	if r00d:
		# stop all sounds playing & load the new file
		mixer.music.load('{}'.format(full_file_path))  
	else: 
		mixer.music.queue('{}'.format(full_file_path))

	# play the new sound
	try:
		print('[SFX] {} played'.format(full_file_path))
		mixer.music.play()
	except TypeError:
		print('TypeError - {} didn\'t play because (assuming) file was not the right type'.format(full_file_path))


###################################################################
# SECTION SFX Generation via folder/file structure bidness
###################################################################

class SoundEffect(object):
	"""
	Base class for all sound effects.

	Eventually looks like ==> SoundEffect(file_name, permission_level, cost, cooldown).
	"""

	# TODO Overriding cooldowns (csv? ORM models?)
	# TODO Attributes: permissions level, cost

	commands = []

	# constructor
	def __init__(self, cmd_name, cmd_path, cmd_timeout=10):
		self.name = cmd_name
		self.path = cmd_path
		# TODO Look into using timedate.timedelta() instead
		self.timeout = cmd_timeout 
		self.last_used = time.time()

		# TODO: Check and see if pre-existing command
		# create/register file as command in event-loop
		@twitch_bot.command(self.name)
		async def sfx_func(message):
			if message.author.subscriber:
				# compare last use to this use & timeout var
				if time.time() - self.last_used >= self.timeout:
					# playsound(self.path) # REVIEW
					play_sfx(self.path)
					# update the last_used thing
					self.last_used = time.time()

		# add the command object to a list to be used later for spreadsheet generation
		SoundEffect.commands.append(self)


# REVIEW  move into a function later during refactor
# for every file in directory (os.listdir(path))
path = 'sfx/hooks/'
for file in os.listdir(path):

	# create instance with attributes
	if file.endswith('.mp3'):
		cmd_name = file[:-4]
		cmd_path = path + file
		debug_msg = 'cmd_name={} cmd_path={}'.format(cmd_name, cmd_path)
		SoundEffect(cmd_name, cmd_path)

# !SECTION             


###################################################################
# SECTION Randomized SFX
###################################################################

class RandomSoundEffect(object):
	"""
	Base class for all rando sound effects.

	Eventually looks like ==> RandoSoundEffect(file_name, permission_level, cost, cooldown).
	"""
	# TODO Overriding cooldowns (csv? ORM models?)
	# TODO Put 'hi' and 'bye' in their own thing? So they can work w/o '!' preface once that's func again
	# TODO Attributes: permissions level, cost

	commands = []

	def generate_csv(self, cmds):
		# REVIEW  what it shoudl REALLY do is just be called from the constructor 
		# and add the command to the next empty line
		
		# TODO check if the command is already in the csv & make it if it doesn't exist (r+)
		# TODO if it isn't, add it

		with open('data/test.csv', 'w+', newline='') as csv_file:
			for cmd in cmds:
				csv_writer = csv.writer(csv_file)
				print('writing {}'.format(cmd.name))
				csv_writer.writerow([cmd.name, cmd.timeout])


	# constructor
	def __init__(self, folder, files:list, aliases=(), cmd_timeout=3):
		self.name = folder
		self.folder = folder
		self.files = files
		self.aliases = aliases
		self.timeout = cmd_timeout
		self.last_used = time.time()

		# TODO: Check and see if pre-existing command
		# create/register file as command in event-loop
		@twitch_bot.command(self.name, alias=self.aliases)
		async def rando_sfx_func(message):
			# compare last use to this use & timeout var
			if time.time() - self.last_used >= self.timeout:
				random_mp3 = 'sfx/randoms/{}/{}'.format(self.folder, random.choice(self.files))
				# playsound(random_mp3) # REVIEW 
				play_sfx(random_mp3)
				# update the last_used thing
				self.last_used = time.time()

		# self.generate_csv()
			
		# add the command name to a list to be used later for spreadsheet generation
		RandomSoundEffect.commands.append(self)



def generate_random_sfx_commands():

	path = 'sfx/randoms/' # TODO change this to something configurable elsewhere for distro stuffs

	# get a list of folders in sfx/randoms & create commands for each
	for thing in os.listdir(path):

		# if directory
		if '.' not in thing or not thing.startswith('.'):
			folder = thing
			files = []

			# create a list of mp3s in folders (excluding aliases.txt)
			for file_name in os.listdir('sfx/randoms/{}'.format(folder)):
				if not file_name.endswith('.txt'):
					# add it to a list
					files.append(file_name)

			# use the above list to create the object thingybob
			RandomSoundEffect(folder, files, get_aliases(folder))
			# TODO CSV "clean" func? Not sure if needed.

		else:
			print('doin it rong')

	RandomSoundEffect.generate_csv(RandomSoundEffect, RandomSoundEffect.commands)


# TODO Get this loading aliases from text files
def get_aliases(folder):
	# loads alias file based on folder name
	try:
		# f = open('sfx/randoms/{}/aliases.txt'.format(folder), 'r')
		# creates a list based on aliases
		# aliases = f.readlines()
		with open('sfx/randoms/{}/aliases.txt'.format(folder), 'r') as f:
			aliases = f.read().splitlines()
		return tuple(aliases)
	except:
		return []


generate_random_sfx_commands()

# !SECTION 


###################################################################
# SECTION Light-reactive SFX
###################################################################

class LEDSoundEffect(object):
	"""
	Base class for all lighted-reactive sound effects.

	Eventually looks like ==> LEDSoundEffect(file_name, permission_level, cost, cooldown).
	"""

	commands = []

	# constructor
	def __init__(self, cmd_name, cmd_path, cmd_char):
		self.cmd = cmd_name
		self.path = cmd_path
		self.char = cmd_char

		# TODO: Check and see if pre-existing command
		# create/register file as command in event-loop
		@twitch_bot.command(self.cmd)
		async def led_sfx_func(message):
			if message.author.subscriber:
				# serial_send.led_fx(self.cmd, self.char) # TODO Arduino stuffs
				# playsound(self.path + self.cmd + '.mp3') # REVIEW 
				play_sfx(self.path + self.cmd + '.mp3')
		
		# add the command name to a list to be used later for spreadsheet generation
		self.commands.append(self.cmd)

# REVIEW move these to UI or something later, so they don't have to be manually set up
def setup_led_commands():
	path = 'sfx/ledcmds/'
	LEDSoundEffect('flashbang', path, 'f')
	LEDSoundEffect('weewoo', path, 'w')

setup_led_commands()

# !SECTION 

###################################################################
# SECTION HELP Function
###################################################################

# TODO Put these in a function. This is repetitive and annoying and unnecesary and I hate myself for it
# and if you judge me you will make me cry cuz I'm sensitive and this r sensitive code. srsbidness.
# (but also it's like not a huge priority js js)

# REVIEW function these out in a refactor
@twitch_bot.command('sfx')
async def sfx(message):
	"""
	Spits out a list of SFX commands. Pretty simple at the moment.
	"""

	# TODO https://github.com/NinjaBunny9000/DeepThonk/issues/26
	
	msg = 'SFX can be used freely by subscribers! :D '

	# for every item in an enumerated list of commands
	for cmd in SoundEffect.commands:
		cmd_name = '!{}'.format(cmd.name) # add the !

		# get the length of the string & compare it to teh length it would be if it added the new command
		if (len(msg) + len(cmd_name) + 2) >= 500:
			# send message and start over
			await twitch_bot.say(message.channel, msg)  # TODO Add page number
			msg = ''
		else:
			# add to msg
			if len(msg) is 0:
				msg += cmd_name
			else:
				msg += ', {}'.format(cmd_name)
	
	# then send the rest
	await twitch_bot.say(message.channel, msg) # TODO add final page number
	# playsound('sfx/sfx.mp3')
	play_sfx('sfx/sfx.mp3')


# REVIEW function these out in a refactor
@twitch_bot.command('randomsfx')
async def randomsfx(message):
	"""
	Spits out a list of RANDOM SFX commands. Pretty simple at the moment.
	"""

	# TODO https://github.com/NinjaBunny9000/DeepThonk/issues/26
	
	msg = 'SFX can be used freely by subscribers! :D '

	# for every item in an enumerated list of commands
	for cmd in RandomSoundEffect.commands:
		cmd_name = '!{}'.format(cmd.name) # add the !

		# get the length of the string & compare it to teh length it would be if it added the new command
		if (len(msg) + len(cmd_name) + 2) >= 500:
			# send message and start over
			await twitch_bot.say(message.channel, msg)  # TODO Add page number
			msg = ''
		else:
			# add to msg
			if len(msg) is 0:
				msg += cmd_name
			else:
				msg += ', {}'.format(cmd_name)
	
	# then send the rest
	await twitch_bot.say(message.channel, msg) # TODO add final page number
	# playsound('sfx/sfx.mp3')
	play_sfx('sfx/sfx.mp3')

# REVIEW function these out in a refactor
@twitch_bot.command('ledsfx')
async def ledsfx(message):
	"""
	Spits out a list of RANDOM SFX commands. Pretty simple at the moment.
	"""

	# TODO https://github.com/NinjaBunny9000/DeepThonk/issues/26
	
	msg = 'SFX can be used freely by subscribers! :D '

	# for every item in an enumerated list of commands
	for cmd in LEDSoundEffect.commands:
		cmd = '!{}'.format(cmd) # add the !

		# get the length of the string & compare it to teh length it would be if it added the new command
		if (len(msg) + len(cmd) + 2) >= 500:
			# send message and start over
			await twitch_bot.say(message.channel, msg)  # TODO Add page number
			msg = ''
		else:
			# add to msg
			if len(msg) is 0:
				msg += cmd
			else:
				msg += ', {}'.format(cmd)
	
	# then send the rest
	await twitch_bot.say(message.channel, msg) # TODO add final page number


# def gen_sfx_list(sfx_type:class):
#     'Returns a list of SFX msgs for the info commands'

#     msg = 'SFX can be used freely by subscribers! :D '

#      # for every item in an enumerated list of commands
#     for cmd in sfx_type.commands:
#         cmd = '!{}'.format(cmd) # add the !

#         # get the length of the string & compare it to teh length it would be if it added the new command
#         if (len(msg) + len(cmd) + 2) >= 500:
#             # send message and start over
#             await twitch_bot.say(message.channel, msg)  # TODO Add page number
#             msg = ''
#         else:
#             # add to msg
#             if len(msg) is 0:
#                 msg += cmd
#             else:
#                 msg += ', {}'.format(cmd)

#     return msg


# !SECTION


###################################################################
# SECTION Debug commands (remove in refactor, etc)
###################################################################


@twitch_bot.command('earwormroulette')
async def earwormroulette(message):

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

###################################################################
# SECTION Debug commands (remove in refactor, etc)
###################################################################
		
@twitch_bot.command('testwaifu')
async def testwaifu(message):
	# playsound('sfx/hooks/waifu.mp3')
	play_sfx('sfx/hooks/waifu.mp3')

@twitch_bot.command('testsfx')
async def testsfx(message):
	path = 'sfx/hooks/'
	file_name = 'ding'
	play_sfx(path, file_name)

@twitch_bot.command('testraidsfx')
async def testraidsfx(message):
	play_sfx('sfx/alerts/raid.mp3')
   

# !SECTION 