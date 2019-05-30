from conf import bot
from utils.logger import loggyballs as log

import sfx

@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')

@bot.event
async def event_message(message):
    await bot.handle_commands(message)

@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
    log.info("test") # test for logging to work
    await ctx.send(f'Hello {ctx.author.name}!') # tests chat


if __name__ == "__main__":
    bot.run()
