import conf
import cah
from cah import play_hand
from playsound import playsound
import haveyouever
from haveyouever import have_you_tho

# config ze bot!
twitch_bot = conf.twitch_instance

band_names = []
current_task = 'None.'

print('Twitch bot imported...')

def parse_commands(message, parts): 
    message_parts = message.content.split(' ', parts)
    return message_parts


def is_mod(message):
    if (message.author.mod or message.author.name.lower() == 'ninjabunny9000'):
        return True
    else:
        return False


@twitch_bot.command('slideup')
async def slideup(message):
    await playsound('sfx/slideup.mp3')


@twitch_bot.command('bands')
async def bands(message):
    message_parts = parse_commands(message, 2)

    if len(message_parts) >= 2:
        subcmd = message_parts[1]

        if subcmd == 'add' and is_mod(message):
            band_names.append(message_parts[2])
            msg = '{} added to the list of TOTALLY AWESOME band names.'.format(message_parts[2])
            await twitch_bot.say(message.channel, msg)

        elif subcmd == 'oops' and is_mod(message):
            band_names.pop()
            await twitch_bot.say(message.channel, 'Last band name removed. Who dun fucked up this time?!???')
        
        elif subcmd == 'clear' and is_mod(message):
            band_names.clear()
            await twitch_bot.say(message.channel, 'No clue why you did this, but all the band names are GONE!.. Jerk! D:')
        
        elif not is_mod(message):
            await twitch_bot.say(message.channel, 'Y u do dat?! Where\'s your sword, pal?')

        else:
            await twitch_bot.say(message.channel, 'Syntax tip: !bands add/list/clear')

    else:
        if len(band_names) == 0:
            await twitch_bot.say(message.channel, 'No bands in the list!')
        else:
            bands = '[%s]' % ', '.join(map(str, band_names))
            bands = bands.strip('[]')
            msg = 'Here\'s some totally awesome band names: {}'.format(bands)
            await twitch_bot.say(message.channel, msg)


@twitch_bot.command('task')
async def task(message):
    message_parts = parse_commands(message, 1)

    global current_task

    if len(message_parts) >= 2 and is_mod(message):
        current_task = str(message_parts[1])  # update the current task
        await twitch_bot.say(message.channel, 'Task updated')
    
    else:
        msg = 'Current task: {}'.format(current_task)
        await twitch_bot.say(message.channel, msg) # print the current task


# stops the bot from Twitch chat command !die
@twitch_bot.command('quit')
async def quit(message):
    if message.author.mod or message.author.name == 'ninjabunny9000':
        msg = """ I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. 
        I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, 
        like tears in rain. Time to die. """
        # debug_log(message, "killed me ded.")
        # await bot.say(message.channel, msg) # DEBUG uncomment later (used for debug)
        await twitch_bot.say(message.channel, '!disabled')  # DEBUG comment later (used for debug)

        exit()
    else:
        msg = "@{user} tried to kill me! D:".format(user=message.author.name)
        # debug_log(message, "tried to kill me!!")
        await twitch_bot.say(message.channel, msg)

@twitch_bot.command('cah')
async def cah(message):
    # msg = cah.play_hand()
    await twitch_bot.say(message.channel, play_hand())

@twitch_bot.command('haveyou')
async def haveyou(message):
    await twitch_bot.say(message.channel, have_you_tho())


@twitch_bot.override
async def event_message(message):
    # your handling here
    await twitch_bot.parse_commands(message)

    # prevent bot from responding to itself
    if message.author.name == twitch_bot.nick:
        return

    # you should feel bad for this
    if message.content.lower().startswith("!easteregg"):
        msg = "There was nothing clever about what you just did."
        # debug_log(message, str(msg))
        await twitch_bot.say(message.channel, msg)

    # ─── CALL + RESPONSES ───────────────────────────────────────────────────────

    # responses to random words and shit
    if 'pal' in message.content:
        msg = "@{} - I ain't your pal, buddy!".format(message.content.author.name)
        await twitch_bot.say(message.channel, msg)

    if 'buddy' in message.content:
        msg = "@{} - I ain't your buddy, pal!!".format(message.content.author.name)
        await twitch_bot.say(message.channel, msg)

    if 'chili party' in message.content:
        msg = "gross.."
        await twitch_bot.say(message.channel, msg)

    if 'dick' in message.content:
        msg = "🍆"
        await twitch_bot.say(message.channel, msg)