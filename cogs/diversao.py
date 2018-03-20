import discord
import random
from discord.ext import commands

class Diversao:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def calcularamor(self, ctx, user1 : discord.Member, user2 : discord.Member = None):
        """Calcula o amor entre 2 membros"""
        if user2 == None:
            user2 = ctx.message.author
        random.seed(user2.id+user1.id)
        rnd = random.randint(1, 10)
        l1 = (len(user1.name))
        l2 = (len(user2.name))
        score = 100 - (l1 * l2) - rnd
        if score > 40:
            heart = "❤"
        else:
            heart = "💔"
        embed = discord.Embed(color=0xDEADBF,
                              title="Calculadora do amor",
                              description=f"{user1.name} {heart} {user2.name} = {score}%")
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def legal(self, ctx, member: discord.Member = None):
        """Informa se você ou o membro marcado é legal"""
        if member is None:
            member = ctx.message.author
        random.seed(member.id)
        result = random.randint(1, 2)
        if result == 2:
            await self.bot.say('Não, {0.mention} não é legal.'.format(member))
        if result == 1:	
            await self.bot.say('Sim, {0.mention} é legal.'.format(member))


def setup(bot):
    bot.add_cog(Diversao(bot))

