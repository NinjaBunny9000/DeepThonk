from conf import bot
from utils.logger import loggyballs as log


@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')

@bot.event
async def event_message(message):
    # print(message.content)
    await bot.handle_commands(message)

@bot.command(name='test', aliases=['t'])
async def test_command(ctx):
    log.info("test")
    await ctx.send(f'Hello {ctx.author.name}')


if __name__ == "__main__":
    bot.run()