from conf import twitch_instance, twitch_channel, streamer, welcome_msg, is_bot_admin, bot_name
import asyncio
from obs_ctrl import change_scene, get_scene
from twitch_permissions import is_bot, is_mod


# config ze bot!
twitch_bot = twitch_instance

# global vars
emote_count = 0

# ─── PLAIN OLE FUNCTIONS ────────────────────────────────────────────────────────




# ─── TRADITIONAL COMMANDS - VIA @COMMANDS ───────────────────────────────────────


# ─── RAID SEQUENCE ──────────────────────────────────────────────────────────────
 
def count_emotes(message):
    for emote in message.emotes:
        global emote_count
        emote_count = emote_count + 1
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

def raid_in_progress(message):
    # chk the message or webhooks for raid triggers
    if "trigger raid" in message.content.lower():
        print("raid in progress")
        
        return True

def keep_score(message):
    emotes = count_emotes(message)
    print("emotes = " + str(emotes))
    return emotes

def reset_emote_count():
    global emote_count
    emote_count = 0

        

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