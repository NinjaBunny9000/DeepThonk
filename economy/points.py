import conf
import data_tools
from integrations.streamelements.api_wrapper import get_points as get_se_points, put_points as put_se_points


# config ze bot!
twitch_bot = conf.twitch_instance


#  get the points of the user that sends message (streamelements atm)
@twitch_bot.command('points')
async def wutpoints(message):
    points = get_se_points(message.author.name)
    msg = f'@{message.author.name}, you have {points} points.'
    await twitch_bot.say(message.channel, msg)


###############################################################################
# ANCHOR  Points gifting system
###############################################################################

if conf.economy['points_gifting']:

    @twitch_bot.command('gift')
    async def gift(message):
        'Change meh'

        token = data_tools.tokenize(message, 3)

        if len(token) <= 2 or token[2].isdigit() == False:
            msg = 'Try !gift <user> <amount>.'
            await twitch_bot.say(message.channel, msg)
            return

        gift = int(token[2])
        gifter = message.author.name
        giftee = data_tools.ats_or_nah(token[1])

        # cehck if gifter has enough points
        if get_se_points(gifter) >= gift:
            # do the exchangey thing
            put_se_points(giftee, gift) # TODO Check to get 404
            put_se_points(gifter, -gift)
            points = get_se_points(gifter)
            msg = f'@{gifter}. You gave {gift} shuriken to @{giftee}!! You have {points} left.'
            await twitch_bot.say(message.channel, msg)

        # otherwise, tell them they don't if they don't have enough points
        else:
            msg = f'While your generosity is greatly apprecaited, @{gifter}, you don\'t seem to have enough points right now.'
            await twitch_bot.say(message.channel, msg)