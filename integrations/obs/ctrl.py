import conf
from integrations.twitch.privilege import is_mod

# config ze bot!
twitch_bot = conf.twitch_instance


###############################################################################
# SECTION OBS Scene Control
###############################################################################

def change_scene(scene):
    """
    **Requires 'Advance Scene Switcher' plug-in**
    Swap scenes in OBS studio by writing the scene name to a file.
    """
    f = open('data\\scene_next.txt', 'w+')
    f.write(scene)
    f.close()


def get_scene():
    """
    **Requires 'Advance Scene Switcher' plug-in**
    Read current scene from OBS studio, which is writing scene names 
    to a .txt file.
    """
    f = open('data\\scene_current.txt', 'r+')
    scene = f.readline()
    f.close()
    return scene


@twitch_bot.command('obsscene')
async def obsscene(message):
    if is_mod(message):
        scene = get_scene()
        msg = f'@{message.author.name}, the current scene is {scene}'
        await twitch_bot.say(message.channel, msg)


@twitch_bot.command('obsbsod')
async def obsbsod(message):
    if is_mod(message):
        change_scene('BSOD')


@twitch_bot.command('afk')
async def afk(message):
    if is_mod(message):
        change_scene(conf.scenes['brb'])


@twitch_bot.command('wb')
async def wb(message):
    if is_mod(message):
        change_scene(conf.scenes['main'])


@twitch_bot.command('obsintro')
async def obsintro(message):
    if is_mod(message):
        change_scene('INTRO')


@twitch_bot.command('obsswap')
async def obsswap(message):
    if is_mod(message):
        change_scene('GAMES SWAP')


@twitch_bot.command('obsraid')
async def obsswobsraidap(message):
    if is_mod(message):
        change_scene('RAID')


@twitch_bot.command('obsraid2')
async def obsraid2(message):
    if is_mod(message):
        change_scene('RAID2')


@twitch_bot.command('obsdj')
async def obsdj(message):
    if is_mod(message):
        change_scene('DJ')


# switch scene to GAMES    
@twitch_bot.command('obsmain')
async def obsmain(message):
    if is_mod(message):
        change_scene('MAIN')
        msg = "Switching scene back to MAIN."
        await twitch_bot.say(message.channel, msg) 

# !SECTION 