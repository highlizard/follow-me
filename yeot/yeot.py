import os
import random
import discord
import asyncio
import time
from .utils import checks
from __main__ import send_cmd_help
from .utils.dataIO import dataIO
from discord.ext import commands


class Yeot:
    """ตังเมสุดยอดต้นตำรับของมิสเทลทีน"""

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/yeot/yeot.json"
        self.system = dataIO.load_json(self.file_path)

    @commands.group(pass_context=True, no_pm=True)
    async def setyeot(self, ctx):
        """Yeot settings group command"""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @setyeot.command(name="yeotcd", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _yeotcd_heist(self, ctx, cooldown: int):
        """Set the cooldown for yeot command"""
        server = ctx.message.server
        settings = self.check_server_settings(server)
        if cooldown >= 0:
            settings["Config"]["Yeot CD"] = cooldown
            dataIO.save_json(self.file_path, self.system)
            msg = "Cooldown for yeot set to {}".format(cooldown)
        else:
            msg = "Cooldown needs to be higher than 0."
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    async def yeot(self, ctx):
        """Obtain a random number of Yeots."""
        author = ctx.message.author
        server = ctx.message.server
        action = "Yeot CD"
        settings = self.check_server_settings(server)
        self.account_check(settings, author)
        if await self.check_cooldowns(author.id, action, settings):
            weighted_sample = [1] * 152 + [x for x in range(49) if x > 1]
            yeots = random.choice(weighted_sample)
            settings["Players"][author.id]["Yeots"] += yeots
            dataIO.save_json(self.file_path, self.system)
            await self.bot.say("อิอิ \nคุณได้รับตังเมสุดยอดต้นตำรับ {} ชิ้น"
                               "จากมิสเทลทีน".format(yeots))

    @commands.command(pass_context=True, no_pm=False, ignore_extra=False)
    async def jar(self, ctx):
        """See how many yeots are in your jar."""
        author = ctx.message.author
        server = ctx.message.server
        settings = self.check_server_settings(server)
        self.account_check(settings, author)
        yeots = settings["Players"][author.id]["Yeotss"]
        await self.bot.whisper("ในโหลมีตังเมสุดยอดต้นตำรับ {} ชิ้น"
                               "".format(yeots))

   


def check_folders():
    if not os.path.exists("data/yeot/yeot"):
        print("Creating data/yeot/yeot folder...")
        os.makedirs("data/yeot/yeot")


def check_files():
    default = {"Servers": {}}

    f = "data/yeot/yeot.json"
    if not dataIO.is_valid_json(f):
        print("Creating default yeot.json...")
        dataIO.save_json(f, default)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Yeot(bot))
