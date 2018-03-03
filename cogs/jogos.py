import discord
import random
from discord.ext import commands

class Jogos:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def moeda(self, ctx):
        """Irá sortear entre cara ou coroa."""
        message = ctx.message
        escolha = random.randint(1, 2)
        if escolha == 1:
            await self.bot.add_reaction(message, '😀')
        if escolha == 2:
            await self.bot.add_reaction(message, '👑')    



def setup(bot):
    bot.add_cog(Jogos(bot))