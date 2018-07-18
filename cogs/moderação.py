import discord, argparse, re, shlex, traceback, io, textwrap, asyncio
from discord.ext import commands
from utils import checks
from contextlib import redirect_stdout
from collections import Counter


class Moderacao:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(guild_only=True, pass_context=True)
    async def delete(self, ctx, amount, channel: discord.Channel=None):
        """Deleta a quantidade de mensagens desejada !delete <quantidade>."""
        if ctx.message.author.server_permissions.manage_messages:
            channel = channel or ctx.message.channel
            deleteds = 0
            total = amount
            try:
                amount = int(amount)
                await self.bot.delete_message(ctx.message)
                if amount > 100:
                    amountdiv = int(amount/100)
                    amountrest = amount-(amountdiv*100)
                    for amount in range(amount, amountrest, -100):
                        deleted = await self.bot.purge_from(channel, limit=amount)
                        deleteds = deleteds + len(deleted)
                else:
                    deleted = await self.bot.purge_from(channel, limit=amount)
                    deleteds = deleteds + len(deleted)
            except ValueError:
                await self.bot.say('Utilize o comando com uma quantidade valida : ```!delete <quantidade>```')
            botmsgdelete = await self.bot.send_message(ctx.message.channel,'Deletei {} mensagens de um pedido de {} no canal {} para {}'.format(deleteds, total, channel.mention,ctx.message.author.mention))
            await asyncio.sleep(5)
            await self.bot.delete_message(botmsgdelete)
        else:
            await self.bot.say('você não possui permissão para usar esse comando')

    @commands.command(guild_only=True, pass_context=True)
    async def kickar(self, ctx, member: discord.Member, *, reason = None):
        """Kicka um membro do servidor."""
        if ctx.message.author.server_permissions.kick_members:
            await self.bot.kick(member)
            await self.bot.say(f'{member.mention} foi kickado do servidor')
        else:
            await self.bot.say('você não possui permissão para usar esse comando')

    @commands.command(guild_only=True, pass_context=True)
    async def banir(self, ctx, member: discord.Member):
        """Bane um membro do servidor."""
        if ctx.message.author.server_permissions.ban_members:
            await self.bot.ban(member)
            await self.bot.say(f'{member.mention} foi banido do servidor')
        else:
            await self.bot.say('você não possui permissão para usar esse comando')

#    @commands.command(guild_only=True, pass_context=True)
#    async def unban(self, ctx, member: discord.User):
#        """Desbane um membro do servidor."""
#        if ctx.message.author.server_permissions.ban_members:        
#            await self.bot.unban(ctx.message.server, member)
#            await self.bot.say(f'{member.name} (ID: {member.id}) Foi desbanido.')
#        else:
#            await self.bot.say('você não possui permissão para usar esse comando')


    @commands.command(pass_context=True, no_pm=True)
    async def mutar(self, ctx, *, member: discord.Member):
        """Muta o membro."""
        if ctx.message.author.server_permissions.mute_members:
            cargomute = discord.utils.find(lambda r: r.name == "Mutado", ctx.message.server.roles)
            await self.bot.add_roles(member, cargomute)
            await self.bot.say(f'o membro {member.mention} foi mutado.')
        else:
            await self.bot.say('você não possui permissão para usar esse comando')

    @commands.command(pass_context=True, no_pm=True)
    async def desmutar(self, ctx, *, member : discord.Member):
        """Desmuta o membro."""
        if ctx.message.author.server_permissions.mute_members:
            cargomute = discord.utils.find(lambda r: r.name == "Mutado", ctx.message.server.roles)
            await self.bot.remove_roles(member, cargomute)
            await self.bot.say(f'o membro {member.mention} foi desmutado.')
        else:
            await self.bot.say('você não possui permissão para usar esse comando')

    @commands.command(guild_only=True, pass_context=True)
    async def presence(self, ctx, *, changeto : str):
        if ctx.message.author.id == "182635477977923585":
            game = discord.Game(name=changeto, url="https://www.twitch.tv/tmpoarr",
                                type=0)
            await self.bot.change_presence(game=game)
        else:
            await self.bot.say('você não possui permissão para usar esse comando')

    @commands.command(guild_only=True, pass_context=True)
    async def renomear(self, ctx, user : discord.Member, *, nickname =""):
        """Altera o apelido de um membro"""
        if ctx.message.author.server_permissions.manage_nicknames:
            if nickname == "":
                nickname = None
            try:
                await self.bot.change_nickname(user, nickname)
                await self.bot.say("Pronto!")
            except discord.Forbidden:
                await self.bot.say("Eu não tenho permissões pra isso :(")
        else:
            await self.bot.say('você não possui permissão para usar esse comando')

def setup(bot):
    bot.add_cog(Moderacao(bot))