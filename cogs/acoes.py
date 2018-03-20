import discord
import aiohttp
import json
import safygiphy
import random
import lxml
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

class Acoes():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def socar(self, ctx, member: discord.Member=None):
        """Soca alguém."""
        user = ctx.message.author.name
        if member is None:
            user = "Megumin"
            member = ctx.message.author
        g = safygiphy.Giphy(token='rener21BaDh2WcIgmARoUpAZcDBAGaR3')
        r = g.search(q="anime punch", limit=25)
        gif_dataa=r['data']
        gif_data=gif_dataa[random.randint(1,20)]
        id=gif_data["id"]
        url = "https://media.giphy.com/media/"+id+"/giphy.gif"
        print(url)
        embed1=discord.Embed(title="{0} socou {1.name}".format(user, member))
        await self.bot.say(embed=embed1.set_image(url=url))

    @commands.command(pass_context=True)
    async def abraçar(self, ctx, member: discord.Member=None):
        """Abraça alguém."""
        user = ctx.message.author.name
        if member is None:
            user = "Megumin"
            member = ctx.message.author
        g = safygiphy.Giphy(token='rener21BaDh2WcIgmARoUpAZcDBAGaR3')
        r = g.search(q="anime hug", limit=25)
        gif_dataa=r['data']
        gif_data=gif_dataa[random.randint(1,20)]
        id=gif_data["id"]
        url = "https://media.giphy.com/media/"+id+"/giphy.gif"
        print(url)
        embed1=discord.Embed(title="{0} abraçou {1.name}".format(user, member))
        await self.bot.say(embed=embed1.set_image(url=url))

    @commands.command(pass_context=True)
    async def beijar    (self, ctx, member: discord.Member=None):
        """Beija alguém."""
        user = ctx.message.author.name
        if member is None:
            user = "Megumin"
            member = ctx.message.author
        g = safygiphy.Giphy(token='rener21BaDh2WcIgmARoUpAZcDBAGaR3')
        r = g.search(q="anime kiss", limit=25)
        gif_dataa=r['data']
        gif_data=gif_dataa[random.randint(1,20)]
        id=gif_data["id"]
        url = "https://media.giphy.com/media/"+id+"/giphy.gif"
        print(url)
        embed1=discord.Embed(title="{0} beijou {1.name}".format(user, member))
        await self.bot.say(embed=embed1.set_image(url=url))

    @commands.command(pass_context=True)
    async def carinho(self, ctx, member: discord.Member=None):
        """Faz carinho em alguém."""
        user = ctx.message.author.name
        if member is None:
            user = "Megumin"
            member = ctx.message.author
        g = safygiphy.Giphy(token='rener21BaDh2WcIgmARoUpAZcDBAGaR3')
        r = g.search(q="anime rub", limit=25)
        gif_dataa=r['data']
        gif_data=gif_dataa[random.randint(1,20)]
        id=gif_data["id"]
        url = "https://media.giphy.com/media/"+id+"/giphy.gif"
        print(url)
        embed1=discord.Embed(title="{0} fez carinho em {1.name}".format(user, member))
        await self.bot.say(embed=embed1.set_image(url=url))


def setup(bot):
    bot.add_cog(Acoes(bot))