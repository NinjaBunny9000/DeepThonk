import random
import os

# internal modules & packages
import conf
import data_tools
from integrations.twitch.privilege import is_bot, is_mod
from sfx.sfx import play_sfx

# # config ze bot!
twitch_bot = conf.twitch_instance


if conf.modules['lists']:

    ###############################################################################
    # SECTION Bands
    ###############################################################################

    if conf.lists['bands']:

        @twitch_bot.command('bands')
        async def bands(message):
            'Works similar to quotes, but tracks TOTALLY AWESOME band names.'

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

        @twitch_bot.command('smrt')
        async def smrt(message):
            token = data_tools.tokenize(message, 1, lower_case=False)
            if len(token) > 1:
                # check permissions
                if is_mod(message):
                    # add token/quote to file thingy
                    data_tools.add_to_txt(
                        'data/lists/', 
                        'smrt.txt', 
                        token[1], 
                        lower_case=False
                        )
            else:
                comments = data_tools.txt_to_list('data/lists/', 'smrt.txt')
                # create a list of mp3s in folder
                files = []
                for file_name in os.listdir(f'sfx/randoms/smrt'):
                    files.append(file_name)
                random_mp3 = f'sfx/randoms/smrt/{random.choice(files)}'
                play_sfx(random_mp3)
                msg = f'@{message.author.name}: "{str(random.choice(comments))}"'
                msg = f'"{str(random.choice(comments))}"'
                await twitch_bot.say(message.channel, msg)

    # !SECTION