import conf

# config ze bot!
twitch_bot = conf.twitch_instance


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