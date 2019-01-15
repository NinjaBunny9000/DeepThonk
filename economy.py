import conf
from conf import twitch_instance
import api_integrations
import data_tools

# config ze bot!
twitch_bot = twitch_instance

if conf.economy['streamelements_points']:

    #  get the points of the user that sends message (streamelements atm)
    @twitch_bot.command('points')
    async def wutpoints(message):
        points = api_integrations.get_points(message.author.name)
        msg = f'@{message.author.name}, you have {points} points.'
        await twitch_bot.say(message.channel, msg)


###############################################################################
# SECTION Points gifting system
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
        giftee = token[1]

        # cehck if gifter has enough points
        if api_integrations.get_points(gifter) >= gift:
            # do the exchangey thing
            api_integrations.put_points(giftee, gift) # TODO Check to get 404
            api_integrations.put_points(gifter, -gift)
            points = api_integrations.get_points(gifter)
            msg = f'@{gifter}. You gave {gift} shuriken to @{giftee}!! You have {points} left.'
            await twitch_bot.say(message.channel, msg)

        # otherwise, tell them they don't if they don't have enough points
        else:
            msg = f'While your generosity is greatly apprecaited, @{gifter}, you don\'t seem to have enough points right now.'
            await twitch_bot.say(message.channel, msg)

# !SECTION 