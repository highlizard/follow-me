import discord
from discord.ext import commands
from __main__ import send_cmd_help
import aiohttp

class rndcat:
    def __init__(self, bot):
        self.bot = bot
       
    async def listener(self, message):
        channel = message.channel
        if message.author.id != self.bot.user.id:
            if message.content.lower().startswith('ccat') or message.content.lower().startswith('aayy'):
                search = "http://random.cat/meow"
                try:
                     async with aiohttp.get(search) as r:
                result = await r.json()
            await self.bot.say(result['file'])
                except:
            await self.bot.say("Couldnt Get An Image")


def setup(bot):
    n = rndcat(bot)
    bot.add_listener(n.listener, "on_message")
    bot.add_cog(n)
