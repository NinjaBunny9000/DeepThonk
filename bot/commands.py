import json
from logger import log


class SimpleCommand:

    def __init__(self, bot, cmd):
        @bot.command(name=cmd['name'], aliases=cmd['aliases'])
        async def importedCommand(ctx):
            if CommandManager.checkPermissions(ctx):
                pass
            response = cmd['response']
            await ctx.send(response)

class FAQ:

class CommandManager:

    def __init__(self, bot):
        self.bot = bot
        self.list = []

    def importCommands(self, file):
        self.registerCommands(self.getCommands(file))

    def importFAQ(self, file):
        self.registerFAQ(self.getFAQ(file))

    @staticmethod
    def getFAQ(file):
        with open(file) as json_file:
            return json.load(json_file)

    def registerFAQ(self, faqs):
        for faq in faqs:
            SimpleCommand(self.bot, faq)

    @staticmethod
    def getCommands(file):
        with open(file) as json_file:
            return json.load(json_file)['commands']

    def registerCommands(self, cmds):
        for cmd in cmds:
            SimpleCommand(self.bot, cmd)
            self.list.append(cmd['name'])
        log.debug(f"Commands imported from JSON data: {self.list}")

    # todo
    def checkPermissions(ctx):
        pass

    # todo
    def generateCmdList(self):
        pass
