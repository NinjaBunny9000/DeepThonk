import asynctwitch
import twitch_chat
import conf

# config ze bot!
twitch_bot = conf.twitch_instance

class Command(object):
    """Base class for all commands."""

    # constructor
    def __init__(self, cmd, response_msg='Roger roger.', mod=0):
        self.cmd = cmd
        self.response = response_msg
        self.mods_only = mod
     
        @twitch_bot.command(self.cmd)
        async def cmd_func(message):
            print(self.response)
            await twitch_bot.say(message.channel, self.response)
        
    
    def report(self):
        print(self.cmd)

test = Command('test', 'test passed', 0)
testies = Command('testies', 'both testies are intact', 0)






