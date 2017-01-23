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
        
    @commands.command(pass_context=True, no_pm=True)
    async def steal(self, ctx, user: discord.Member=None):
        """Steal cookies from another user. 2h cooldown."""
        author = ctx.message.author
        server = ctx.message.server
        action = "Steal CD"
        settings = self.check_server_settings(server)
        self.account_check(settings, author)
        if not user:
            users = [server.get_member(x) for x in settings["Players"].keys() if x != author.id and x in settings["Players"].keys()]
            users = [x for x in users if settings["Players"][x.id]["Yeots"] > 0]
            if not users:
                user = "Fail"
            else:
                user = random.choice(users)
                self.account_check(settings, user)
        if await self.check_cooldowns(author.id, action, settings):
            if user == "Fail":
                msg = "ω(=OｪO=)ω Nyaaaaaaaan! I couldn't find anyone with yeots!"
            elif settings["Players"][user.id]["Yeots"] == 0:
                msg = ("ω(=｀ｪ ´=)ω Nyaa! Neko-chan is sorry, nothing but crumbs in this human's "
                       ":cookie: jar!")
            else:
                success_chance = random.randint(1, 100)
                if success_chance <= 90:
                    yeot_jar = settings["Players"][user.id]["Yeots"]
                    yeots_stolen = int(cookie_jar * 0.75)
                    if yeots_stolen == 0:
                        yeots_stolen = 1
                    stolen = random.randint(1, yeots_stolen)
                    settings["Players"][user.id]["Yeots"] -= stolen
                    settings["Players"][author.id]["Yeots"] += stolen
                    dataIO.save_json(self.file_path, self.system)
                    msg = ("ω(=＾ ‥ ＾=)ﾉ彡:cookie:\nYou stole {} yeots from "
                          "{}!".format(stolen, user.name))
                else:
                    msg = ("ω(=｀ｪ ´=)ω Nyaa... Neko-chan couldn't find their :cookie: jar!")
            await self.bot.say("ଲ(=(|) ɪ (|)=)ଲ Neko-chan is on the prowl to steal :cookie:")
            await asyncio.sleep(3)
            await self.bot.say(msg)

    def account_check(self, settings, userobj):
        if userobj.id not in settings["Players"]:
            settings["Players"][userobj.id] = {"Yeots": 0,
                                               "Steal CD": 0,
                                               "Yeot CD": 0}
            dataIO.save_json(self.file_path, self.system)

    async def check_cooldowns(self, userid, action, settings):
        path = settings["Config"][action]
        if abs(settings["Players"][userid][action] - int(time.perf_counter())) >= path:
            settings["Players"][userid][action] = int(time.perf_counter())
            dataIO.save_json(self.file_path, self.system)
            return True
        elif settings["Players"][userid][action] == 0:
            settings["Players"][userid][action] = int(time.perf_counter())
            dataIO.save_json(self.file_path, self.system)
            return True
        else:
            s = abs(settings["Players"][userid][action] - int(time.perf_counter()))
            seconds = abs(s - path)
            remaining = self.time_formatting(seconds)
            await self.bot.say("This action has a cooldown. You still have:\n{}".format(remaining))
            return False

    def time_formatting(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        msg = "```{} hours, {} minutes and {} seconds remaining```".format(h, m, s)
        return msg

    def check_server_settings(self, server):
        if server.id not in self.system["Servers"]:
            self.system["Servers"][server.id] = {"Players": {},
                                                 "Config": {"Steal CD": 5,
                                                            "Yeot CD": 5}
                                                 }
            dataIO.save_json(self.file_path, self.system)
            print("Creating default heist settings for Server: {}".format(server.name))
            path = self.system["Servers"][server.id]
            return path
        else:
            path = self.system["Servers"][server.id]
            return path

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
