import discord

from discord.ext import commands


class MistelteinBot:                                                              #change the classname
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True, pass_context=True)
    async def misteltein(self, ctx):                                              #change the command that starts the function
        """
        Shows bot info about riceBot"""
        channel = ctx.message.channel
        msg = '```asciidoc\n'
        msg += '\n\nWhat is MistelteinBot? :: '                                   #change the name of riceBot to name of your bot
        msg += '\nA Bot for CLOSERS Online player.'
        msg += 'The bot is currently on '
        msg += str(len(self.bot.servers))
        msg += ' Servers and connected to '
        msg += str(len(set(self.bot.get_all_members())))
        msg += ' users.\nHere is a list of basic commands:'
        msg += '\n```'
        msg += '```md\n'
        msg += '< Get help      = use m.help or m.help [command] >\n'
        msg += '\n```'
        await self.bot.say(msg)

       
    async def on_server_join(self, server):
        msg = "```asciidoc\n"
        msg += "Announcement :: Information\n"
        msg += "= -=-=-=-=-=-=-=-=-=-=-=- =\n"
        msg += "Thank you for inviting Misteltein!\n"
        msg += "For basic information on the bot, a list of commands, or to contact the owner, use: \n"
        msg += "= m.help =\n"
        msg += "= rice.contact =\n"
        msg += "\n```"
        try:
            await self.bot.send_message(server, msg)
        except:
            pass


def setup(bot):
    n = MistelteinBot(bot)
    bot.add_listener(n.on_server_join)
    bot.add_cog(n)                                               #change the name to what you changed the classname to in line 7
