import sys

import discord
from discord.ext import commands
import asyncio

from discord_conf import token
from discord_conf import server_id

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

# bot = discord.Client()
bot = commands.Bot(command_prefix='!', description=description)

def start_bot():
    bot.run(token)


@bot.event
async def on_ready():
    print('-------------------------------------------------------')
    print(f'Logged in as {bot.user.name} on Ninja\'s Server')
    print('-------------------------------------------------------')


# Automagically add roles to users upon joining
@bot.event
async def on_member_join(member):
    print(f'{member.name} just joined the server!')
    role = discord.utils.get(member.server.roles, name='🔴 LIVE')
    await bot.add_roles(member, role)
    role = discord.utils.get(member.server.roles, name='🔴 LIVE Community Stream!')
    await bot.add_roles(member, role)
    role = discord.utils.get(member.server.roles, name='Ninjas')
    await bot.add_roles(member, role)


# SECTION on_message event loop

@bot.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await bot.send_message(message.channel, 'Calculating messages...')
        async for log in bot.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await bot.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await bot.send_message(message.channel, 'Done sleeping')

    await bot.process_commands(message)

# !SECTION on_message


@bot.command(pass_context=True)
async def roles(ctx):
    'List roles a user has (except @everyone)'
    message = ctx.message
    print('Role command called.')
    member_roles = []
    for role in message.author.roles:
        member_roles.append(role.name)
    print(member_roles)
    msg = f'Roles: {member_roles[1:]}'
    await bot.say(msg)


@bot.command(pass_context=True)
async def livesub(ctx):
    message = ctx.message
    user = message.author.mention
    role = discord.utils.get(message.server.roles, name='🔴 LIVE')
    await bot.add_roles(message.author, role)
    await bot.say(f"You've been added to the 🔴 LIVE role, {user}")


@bot.command(pass_context=True)
async def liveunsub(ctx):
    message = ctx.message
    user = message.author.mention
    role = discord.utils.get(message.server.roles, name='🔴 LIVE')
    await bot.remove_roles(message.author, role)
    await bot.say(f"You've been removed from the 🔴 LIVE role, {user}")


@bot.command(pass_context=True)
async def subs(ctx):
    'List alerts user is subscribed to.'
    message = ctx.message
    user = message.author.mention

    alerts = ['🔴 LIVE', '🔴 LIVE Community Stream!']
    subbed_alerts = []

    for role in message.author.roles:
        if role.name in alerts:
            subbed_alerts.append(role.name)

    subbed_alerts = "\n".join(subbed_alerts)
    msg = f"""{user}, you're subscribed to the following server alerts:

```
{subbed_alerts}
```"""
    await bot.say(msg)


"""
Hi, @user. You're subscribed to the following alerts:
    ```
    🔴 LIVE
    🔴 LIVE Community Stream!
    ```

"""

@bot.command(pass_context=True)
async def debug(ctx):
    print(dir(ctx.message))


if __name__ == '__main__':
    start_bot()
