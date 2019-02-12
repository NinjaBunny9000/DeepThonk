import sys
import os
import random

# internal modules & packages
import conf
from integrations.twitch.privilege import is_bot, is_mod
import data_tools
import integrations.obs.ctrl


# config ze bot!
twitch_bot = conf.twitch_instance


###############################################################################
# SECTION Tasks
###############################################################################

if conf.lists['task']:

    def display_task(task):
        stringyboi = f'!task = {task}'
        data_tools.string_to_txt('data/lists/tasks/', 'current_task.txt', stringyboi, lower_case=False)


    @twitch_bot.command('task')
    async def task(message):
        """
        Keep track of what task you're currently workin on during stream. (WIP: needs to
        connect to db)
        """

        token = data_tools.tokenize(message, 1, lower_case=False) 

        if len(token) >= 2 and is_mod(message):
            current_task = str(token[1])[:250]  # update the current task
            data_tools.add_to_txt('data/lists/tasks/', 'prev_tasks.txt', current_task, lower_case=False)
            display_task(current_task)
            await twitch_bot.say(message.channel, 'Task updated')
        
        else:
            current_task = data_tools.txt_to_string('data/lists/tasks/', 'current_task.txt')
            msg = f'Current task: {current_task}'
            await twitch_bot.say(message.channel, msg) # print the current task


    @twitch_bot.command('randomtask')
    async def randomtask(message):
        tasks = data_tools.txt_to_list('data/lists/tasks/', 'current_task.txt')
        msg = f'@{message.author.name}: "{str(random.choice(tasks))}"'
        await twitch_bot.say(message.channel, msg) # print the current task

# !SECTION