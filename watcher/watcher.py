from __main__ import send_cmd_help
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
import datetime
import discord
import time
import os


class Watcher:
    """
    Be like the Stasi and keep tabs on every member on the server.
    """
    def __init__(self, bot):
        self.bot = bot
        self.settings_file = 'data/watcher/settings.json'
        self.passports_file = 'data/watcher/passports.json'

    @commands.group(pass_context=True, name='border', aliases=[])
    @checks.mod_or_permissions(administrator=True)
    async def _watcher(self, context):
        if context.invoked_subcommand is None:
            await send_cmd_help(context)

    @_watcher.command(pass_context=True, name='setup')
    async def _setup(self, context, channel: discord.Channel):
        """
        Setup a channel
        """
        server = context.message.server
        data = fileIO(self.settings_file, 'load')
        if server.id not in data:
            data[server.id] = {}
        data[server.id]['CUSTOMS_CHANNEL'] = channel.id
        fileIO(self.settings_file, 'save', data)
        message = ':eyes: Done!'
        await self.bot.say(message)

    @_watcher.command(pass_context=True, name='unset', aliases=[])
    async def _clean_setup(self, context):
        """
        Remove channel from this server.
        """
        server = context.message.server
        data = fileIO(self.settings_file, 'load')
        if server.id not in data:
            data[server.id] = {}
        data[server.id]['CUSTOMS_CHANNEL'] = False
        fileIO(self.settings_file, 'save', data)
        message = 'Unset'
        await self.bot.say(message)

   
    @commands.command(pass_context=True, name='passport', aliases=[])
    @checks.mod_or_permissions(kick_members=True)
    async def _member_passport(self, context, member: discord.Member):
        """
        Show previous events (Need kick permissions)
        """
        server = context.message.server
        data = fileIO(self.settings_file, 'load')
        passports = fileIO(self.passports_file, 'load')
        if server.id in data:
            if data[server.id]['CUSTOMS_CHANNEL']:
                if server.id not in passports:
                    passports[server.id] = {}
                if member.id in passports[server.id]:
                    passport = passports[server.id][member.id]
                    now_created = time.time() - time.mktime(datetime.datetime.strptime(str(member.created_at), "%Y-%m-%d %H:%M:%S.%f").timetuple())
                    avatar = member.avatar_url if member.avatar else member.default_avatar_url
                    em = discord.Embed(color=discord.Color.green())
                    em.set_author(name='Passport of {}#{} ({})'.format(member.display_name, member.discriminator, member.id), icon_url=avatar)
                    em.add_field(name='**Created**', value='{}\n({} days ago)'.format(str(member.created_at).split('.')[0], int(now_created / 86400)))
                    em.add_field(name='**Strikes**', value=str(passport['STRIKES']))
                    em.add_field(name='**History**', value='===========', inline=False)

                    for timestamp in sorted(passport):
                        if timestamp != 'BAN' and timestamp != 'STRIKES':
                            if passport[timestamp]['EVENT'] == 'BAN' or passport[timestamp]['EVENT'] == 'STRIKE':
                                em.add_field(name='**{} ({})**'.format(passport[timestamp]['TIMESTAMP'], passport[timestamp]['EVENT']), value='({}) {}'.format(passport[timestamp]['BY_ADMIN'], passport[timestamp]['REASON']))
                            else:
                                em.add_field(name='**{}**'.format(passport[timestamp]['TIMESTAMP']), value=passport[timestamp]['EVENT'])
                    await self.bot.say(embed=em)
                else:
                    await self.bot.say('**Who?**')
        else:
            await self.bot.say('Please run `bordersetup` first!')

  

    async def _on_member_join(self, member):
        server = member.server
        data = fileIO(self.settings_file, 'load')
        passports = fileIO(self.passports_file, 'load')
        timestamp = str(time.time())

        if server.id in data:
            if data[server.id]['CUSTOMS_CHANNEL']:
                channel = data[server.id]['CUSTOMS_CHANNEL']
                customs_channel = discord.utils.get(self.bot.get_all_channels(), id=channel)
                if server.id not in passports:
                    passports[server.id] = {}
                if member.id not in passports[server.id]:
                    passports[server.id][member.id] = {}
                    passports[server.id][member.id]['BAN'] = False
                    passports[server.id][member.id]['STRIKES'] = 0
                passports[server.id][member.id][timestamp] = {}
                passports[server.id][member.id][timestamp]['TIMESTAMP'] = str(time.strftime('%Y-%m-%d %H:%M:%S'))
                passports[server.id][member.id][timestamp]['EVENT'] = 'JOIN'
                passports[server.id][member.id][timestamp]['MEMBER_NAME'] = member.name
                passports[server.id][member.id][timestamp]['MEMBER_ID'] = member.id
                fileIO(self.passports_file, 'save', passports)
                avatar = member.avatar_url if member.avatar else member.default_avatar_url
                em = discord.Embed(color=discord.Color.green())
                em.set_author(name='Guten Tag!! {}#{}'.format(member.display_name, member.discriminator), icon_url=avatar)
                await self.bot.send_message(customs_channel, embed=em)

   
    async def _on_member_remove(self, member):
        server = member.server
        data = fileIO(self.settings_file, 'load')
        passports = fileIO(self.passports_file, 'load')
        timestamp = str(time.time())
        if server.id in data:
            if data[server.id]['CUSTOMS_CHANNEL']:
                channel = data[server.id]['CUSTOMS_CHANNEL']
                customs_channel = discord.utils.get(self.bot.get_all_channels(), id=channel)
                if server.id not in passports:
                    passports[server.id] = {}
                if member.id not in passports[server.id]:
                    passports[server.id][member.id] = {}
                    passports[server.id][member.id]['BAN'] = False
                    passports[server.id][member.id]['STRIKES'] = 0
                passports[server.id][member.id][timestamp] = {}
                passports[server.id][member.id][timestamp]['TIMESTAMP'] = str(time.strftime('%Y-%m-%d %H:%M:%S'))
                passports[server.id][member.id][timestamp]['EVENT'] = 'LEAVE'
                passports[server.id][member.id][timestamp]['MEMBER_NAME'] = member.name
                passports[server.id][member.id][timestamp]['MEMBER_ID'] = member.id
                fileIO(self.passports_file, 'save', passports)
                avatar = member.avatar_url if member.avatar else member.default_avatar_url
                em = discord.Embed(color=discord.Color.green())
                em.set_author(name='Auf Wiedersehen {}#{}'.format(member.display_name, member.discriminator, member.id), icon_url=avatar)
                await self.bot.send_message(customs_channel, embed=em)


def check_folder():
    if not os.path.exists('data/watcher'):
        print('Creating data/watcher folder...')
        os.makedirs('data/watcher')


def check_file():
    data = {}
    settings_file = 'data/watcher/settings.json'
    passports_file = 'data/watcher/passports.json'
    if not fileIO(settings_file, 'check'):
        print('Creating default settings.json...')
        fileIO(settings_file, 'save', data)
    if not fileIO(passports_file, 'check'):
        print('Creating default passports.json...')
        fileIO(passports_file, 'save', data)


def setup(bot):
    check_folder()
    check_file()
    n = Watcher(bot)
    bot.add_listener(n._on_member_join, "on_member_join")
    bot.add_listener(n._on_member_remove, "on_member_remove")
    bot.add_cog(n)
