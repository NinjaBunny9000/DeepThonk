import conf
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

if conf.lists['task']:

    def update_task_at_launch():
        task = db_query.get_latest_task()
        f = open('data\\task.txt', 'w+')
        f.write(f'!task = {task.description}')
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
            msg = f'Current task: {db_query.get_latest_task()}'
            await twitch_bot.say(message.channel, msg) # print the current task


    @twitch_bot.command('randomtask')
    async def randomtask(message):
        await twitch_bot.say(message.channel, str(db_query.rand_task())) # print the current task

# !SECTION


###############################################################################
# SECTION Bands
###############################################################################

if conf.lists['bands']:

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
                msg = f'{token[2]} added to the list of TOTALLY AWESOME band names.'
                await twitch_bot.say(message.channel, msg)
    
            # syntax halpz
            else:
                await twitch_bot.say(message.channel, 'Syntax tip: !bands or !bands add <name>')

        else:
            if len(band_names) == 0:
                await twitch_bot.say(message.channel, 'No bands in the list!')
            else:            
                msg = f'@{message.author.name}, "{random.choice(band_names)}"'
                await twitch_bot.say(message.channel, msg)

# !SECTION


###############################################################################
# SECTION Movie Night
###############################################################################

if conf.lists['movienight']:

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

if conf.lists['comments']:

    @twitch_bot.command('comment')
    async def comment(message):
        comments = data_tools.txt_to_list('data/lists/', 'comments.txt')
        msg = f'@{message.author.name}: "{str(random.choice(comments))}"'
        await twitch_bot.say(message.channel, msg)

# !SECTION