from conf import twitch_instance, twitch_channel, streamer, welcome_msg
from privilege import is_bot, is_mod
import data_tools
import db_query
import db_insert
import content
import obs_ctrl
import random

# config ze bot!
twitch_bot = twitch_instance


###############################################################################
# SECTION Tasks
###############################################################################

def update_task_at_launch():
    task = db_query.get_latest_task()
    f = open('data\\task.txt', 'w+')
    f.write('!task = {}'.format(task.description))
    f.close()

update_task_at_launch()


@twitch_bot.command('task')
async def task(message):
    """
    Keep track of what task you're currently workin on during stream. (WIP: needs to
    connect to db)
    """
    message_parts = data_tools.tokenize(message, 1) 

    if len(message_parts) >= 2 and is_mod(message):
        current_task = str(message_parts[1])[:250]  # update the current task
        db_insert.add_task(current_task)
        # TODO call this at launch, too
        obs_ctrl.display_task_on_obs(current_task)
        await twitch_bot.say(message.channel, 'Task updated')
    
    else:
        msg = 'Current task: {}'.format(db_query.get_latest_task())
        await twitch_bot.say(message.channel, msg) # print the current task


@twitch_bot.command('randomtask')
async def randomtask(message):
    await twitch_bot.say(message.channel, str(db_query.rand_task())) # print the current task


###############################################################################
# !SECTION Bands
###############################################################################




@twitch_bot.command('bands')
async def bands(message):
    """
    Works similar to quotes, but tracks TOTALLY AWESOME band names. Still a WIP, 
    needs to connect to the database, that kind of stuff.
    """
    token = data_tools.tokenize(message, 2, lower_case=False)

    band_names = data_tools.txt_to_list('data/lists/', 'bands.txt')

    if len(token) >= 2:

        subcmd = token[1]

        # !bands (permission check failure)
        if not is_mod(message):
            await twitch_bot.say(message.channel, 'Y u do dat?! Where\'s your sword, pal?')
            return

        # !bands add
        elif subcmd == 'add' and is_mod(message):
            band_names.append(token[2])
            data_tools.add_to_txt('data/lists/', 'bands.txt', token[2])
            msg = '{} added to the list of TOTALLY AWESOME band names.'.format(token[2])
            await twitch_bot.say(message.channel, msg)
 
        # syntax halpz
        else:
            await twitch_bot.say(message.channel, 'Syntax tip: !bands or !bands add <name>')

    else:
        if len(band_names) == 0:
            await twitch_bot.say(message.channel, 'No bands in the list!')
        else:            
            msg = '@{}, "{}"'.format(message.author.name, random.choice(band_names))
            await twitch_bot.say(message.channel, msg)


###############################################################################
# SECTION Have You Ever
###############################################################################

@twitch_bot.command('hye')
async def haveyou(message):
    """
    Have you ever []??? Legitimate questions only.
    """
    #! function is disabled for now:
    await twitch_bot.say(message.channel, content.function_disabled())
    # message_parts = data_tools.tokenize(message, 1)

    # if len(message_parts) >= 2 and is_mod(message):
    #     db_insert.add_hye(str(message_parts[1]), message.author.name)
    #     await twitch_bot.say(
    #         message.channel,
    #         '{} added: "Have you ever {}?"'.format(message.author.name, message_parts[1])
    #         )

    # else:
    #     msg = 'Have you ever ' + db_query.rand_hye().item + '?'
    #     await twitch_bot.say(message.channel, msg) # print the current task


###############################################################################
# !SECTION Reward System
###############################################################################

@twitch_bot.command('reward')
async def reward(message):
    """
    Rewards followers/subs with whatever reward currnetly is for the strem.

    !reward <user> <fol/sub>
    """
    # TODO Validation for members in the room

    # global dict for rewards
    reward_register = data_tools.txt_to_list('data/', 'reward_list.txt')
    
    token = data_tools.tokenize(message, 2, lower_case=False)

    
    # if just `!reward`, list people in teh rewards
    if len(token) is 1:
        if len(reward_register) >= 1:
            # list peeps in the cue
            rewardees = data_tools.stringify_list(reward_register, '@')
            msg = '@{}, these rad folks are qeueued for rewards! {}'.format(message.author.name, rewardees)
        else:
            msg = ' @{}, no community members are queued for rewards (yet).'.format(message.author.name)
        
        await twitch_bot.say(message.channel, msg)
        return

    # spit out how many peeps in teh queue
    if 'qty' == token[1]:
        msg = '{} rad dudes in teh queue'.format(len(reward_register))
        await twitch_bot.say(message.channel, msg)
        return

    if not is_mod(message):
        # TODO Drop this into a function that spits out a standard response for lack of priveglage
        msg = "Sorry, @{}, you can't do unless you're as a mod.".format(message.author.name)
        await twitch_bot.say(message.channel, msg)
        return

    # clear the list if rewards rewarded
    if 'clear' == token[1]:
        data_tools.clear_txt('data/', 'reward_list.txt')
        msg = 'Rewards delivered!!! @{} cleared the list. Thx for bein rad, dudes!'.format(message.author.name)
        await twitch_bot.say(message.channel, msg)
        return

    # add the person to the list
    else:
        data_tools.add_to_txt('data/','reward_list.txt', token[1]) # new hotness
        # reward_register.append(token[1]) # old and busted
        msg = '@{} registered in the reward cue!'.format(token[1])
        await twitch_bot.say(message.channel, msg)


###############################################################################
# SECTION Movie Night
###############################################################################

@twitch_bot.command('movienight')
async def movienight(message):

    token = data_tools.tokenize(message, 1, lower_case=False)
    movies = data_tools.txt_to_list('data/lists/', 'movie_night.txt')

    if len(token) == 1:
        # spit out random movie from the list
        msg = f'@{message.author.name}, "{str(random.choice(movies))[:-1]}" was picked randomly from teh list.'
    else:
        # add the movie to the list
        data_tools.add_to_txt('data/lists/', 'movie_night.txt', token[1])
        msg = f'@{message.author.name}, "{token[1]}" was added to the list!'
    await twitch_bot.say(message.channel, msg)

# !SECTION 


###############################################################################
# SECTION Comments
###############################################################################

@twitch_bot.command('comment')
async def comment(message):
    comments = data_tools.txt_to_list('data/lists/', 'comments.txt')
    msg = f'@{message.author.name}: "{str(random.choice(comments))}"'
    await twitch_bot.say(message.channel, msg)

# !SECTION 