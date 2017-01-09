import discord
from discord.ext import commands
from __main__ import send_cmd_help
import aiohttp

class rndcat:
    """ร่างกายต้องการแมว"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cats(self):
        """Shows a cat"""
        search = "http://random.cat/meow"
        try:
            async with aiohttp.get(search) as r:
                result = await r.json()
            await self.bot.say(result['file'])
        except:
            await self.bot.say("Couldn't Get any cat")
            
def setup(bot):
    n = rndcat(bot)
    bot.add_cog(n)
