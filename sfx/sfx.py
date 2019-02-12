
import os, random, time
import csv
import contextlib
with contextlib.redirect_stdout(None):
    from pygame import mixer


# internal modules & packages
import conf
import games.raid


# config ze bot!
twitch_bot = conf.twitch_instance

mixer.init(frequency=44100)


def play_sfx(full_file_path, r00d=True, unr00dable=False):
	'Interrupts any sound being played and plays the new one that\'s passed in'
	# TODO additional argument for interruptability or nah

	# prevent trampling over raid routine
	if full_file_path == 'sfx/events/raid_victory.mp3':
		pass

	elif games.raid.start():
		# print(f'SFX ABORTED {full_file_path}') # TODO Logging refactor
		return

	if r00d:
		# stop all sounds playing & load the new file
		mixer.music.load(f'{full_file_path}')  
	else: 
		mixer.music.queue(f'{full_file_path}')

	# play the new sound
	try:
		# print(f'[SFX] {full_file_path} played') # TODO Logging refactor
		mixer.music.play()
	except TypeError:
		print(f'TypeError - {full_file_path} didn\'t play because (assuming) file was not the right type') # TODO Logging refactor


def play_random(folder_path):

	files = []

	for thing in os.listdir(folder_path):
		for thing in os.listdir(f'{folder_path}'):
			# add it to a list
			files.append(thing)

	random_mp3 = f'{folder_path}{random.choice(files)}'
	play_sfx(random_mp3)


###################################################################
# SECTION SFX Generation via folder/file structure bidness
###################################################################

class SoundEffect(object):
	'Base class for all sound effects.'

	# TODO Overriding cooldowns (csv? ORM models?)
	# TODO Attributes: privilege level, cost

	commands = []

	# constructor
	def __init__(self, cmd_name, cmd_path, cmd_timeout=conf.sfx['hooks_timeout']):
		self.name = cmd_name
		self.path = cmd_path
		# TODO Look into using timedate.timedelta() instead
		self.timeout = cmd_timeout 
		self.last_used = time.time()

		# TODO: Check and see if pre-existing command
		# create/register file as command in event-loop
		@twitch_bot.command(self.name)
		async def sfx_func(message):
			if message.author.subscriber or message.author.name.lower() == 'ninjabunny9000':
				# compare last use to this use & timeout var
				if time.time() - self.last_used >= self.timeout:
					play_sfx(self.path)
					# update the last_used thing
					self.last_used = time.time()
			else:
				# print(f'no permissions! @{message.author.name.lower()}')
				msg = f"@{message.author.name}, sfx are for subscribers only atm. Sorry!"
				await twitch_bot.say(message.channel, msg)

		# add the command object to a list to be used later for spreadsheet generation
		SoundEffect.commands.append(self)


# REVIEW  move into a function later during refactor
path = 'sfx/hooks/'
for file in os.listdir(path):

	# create instance with attributes
	if file.endswith('.mp3'):
		cmd_name = file[:-4]
		cmd_path = path + file
		debug_msg = f'cmd_name={cmd_name} cmd_path={cmd_path}'
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
	# TODO Attributes: privilege level, cost

	commands = []

	# constructor
	def __init__(self, folder, files:list, aliases=(), cmd_timeout=conf.sfx['randoms_timeout']):
		self.name = folder
		self.folder = folder
		self.files = files
		self.aliases = aliases
		self.timeout = cmd_timeout
		self.last_used = time.time()

		# TODO: Check and see if pre-existing command
		# create/register file as command in event-loop
		@twitch_bot.command(self.name, alias=self.aliases, unprefixed=True)
		async def rando_sfx_func(message):
			# compare last use to this use & timeout var
			if time.time() - self.last_used >= self.timeout:
				random_mp3 = f'sfx/randoms/{self.folder}/{random.choice(self.files)}'
				play_sfx(random_mp3)
				# update the last_used thing
				self.last_used = time.time()
			
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
			for file_name in os.listdir(f'sfx/randoms/{folder}'):
				if not file_name.endswith('.txt'):
					# add it to a list
					files.append(file_name)

			# use the above list to create the object thingybob
			RandomSoundEffect(folder, files, get_aliases(folder))


# TODO Get this loading aliases from text files
def get_aliases(folder):
	# loads alias file based on folder name
	try:
		with open(f'sfx/randoms/{folder}/aliases.txt', 'r') as f:
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
	'Base class for all lighted-reactive sound effects.'

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
# this is not fun
def setup_led_commands():
	path = 'sfx/ledcmds/'
	LEDSoundEffect('flashbang', path, 'f')
	LEDSoundEffect('weewoo', path, 'w')

setup_led_commands()

# !SECTION 


###################################################################
# SECTION HELP Function
###################################################################

# TODO Put these in a function

# REVIEW function these out in a refactor
@twitch_bot.command('sfx')
async def sfx(message):
	'Spits out a list of SFX commands. Pretty simple at the moment.'

	# TODO https://github.com/NinjaBunny9000/DeepThonk/issues/26
	
	msg = 'SFX can be used freely by subscribers! :D '

	# for every item in an enumerated list of commands
	for cmd in SoundEffect.commands:
		cmd_name = f'!{cmd.name}' # add the !

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
				msg += f', {cmd_name}'
	
	# then send the rest
	await twitch_bot.say(message.channel, msg) # TODO add final page number
	# playsound('sfx/sfx.mp3')
	play_sfx('sfx/sfx.mp3')


# REVIEW function these out in a refactor
@twitch_bot.command('randomsfx')
async def randomsfx(message):
	'Spits out a list of RANDOM SFX commands. Pretty simple at the moment.'

	# TODO https://github.com/NinjaBunny9000/DeepThonk/issues/26
	
	msg = 'SFX can be used freely by subscribers! :D '

	# for every item in an enumerated list of commands
	for cmd in RandomSoundEffect.commands:
		cmd_name = f'!{cmd.name}' # add the !

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
				msg += f', {cmd_name}'
	
	# then send the rest
	await twitch_bot.say(message.channel, msg) # TODO add final page number
	# playsound('sfx/sfx.mp3')
	play_sfx('sfx/sfx.mp3')


# REVIEW function these out in a refactor
@twitch_bot.command('ledsfx')
async def ledsfx(message):
	'Spits out a list of all the LED-enabled SFX'

	# TODO https://github.com/NinjaBunny9000/DeepThonk/issues/26
	
	msg = 'SFX can be used freely by subscribers! :D '

	# for every item in an enumerated list of commands
	for cmd in LEDSoundEffect.commands:
		cmd = f'!{cmd}' # add the !

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
				msg += f', {cmd}'
	
	# then send the rest
	await twitch_bot.say(message.channel, msg) # TODO add final page number

# !SECTION