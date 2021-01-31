import json


class Cmd:

    def __init__(self, bot, cmd):
        @bot.command(name=cmd['name'], aliases=cmd['aliases'])
        async def generated_cmd(ctx):
            if Commanderator.checkPermissions():
                pass
            response = cmd['response']
            await ctx.send(response)


class Commanderator:

    def __init__(self, bot):
        self.bot = bot

    def generateCmds(self):
        # open up the json and make cmds from each object in the cmds list
        with open('data/commands.json') as json_file:
            cmds = json.load(json_file)['commands']
            for cmd in cmds:
                Cmd(self.bot, cmd)

    # todo
    def checkPermissions(self):
        pass

    # todo
    def generateCmdList(self):
        pass
