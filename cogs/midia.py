import discord
import aiohttp
import json
import safygiphy
import random
import lxml
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

class Midia():
    def __init__(self, bot):
        self.bot = bot
    
    #CAT
    @commands.command(pass_context=True)
    async def cat(self, ctx):
        """Envia um catineo aleatorio."""	
        async with aiohttp.ClientSession() as session:
            async with session.get('http://random.cat/meow') as r:
                if r.status == 200:
                    js = await r.json()
                    await self.bot.say(embed=discord.Embed().set_image(url=js['file']))

    #DOG
    @commands.command(pass_context=True)
    async def dog(self, ctx):
        """Envia um catiorineo aleatorio."""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random')	as r:	
                if r.status == 200:
                    js = await r.json()
                    await self.bot.say(embed=discord.Embed().set_image(url=js['message']))


    #GIF
    @commands.command()
    async def gif(self, *, stag:str):
        """Envia um gif aleatorio com a tag escolhida !gif <tags>."""
        g = safygiphy.Giphy(token='rener21BaDh2WcIgmARoUpAZcDBAGaR3')
        r = g.search(q=stag, limit=25)
        gif_dataa=r['data']
        escolha = random.randint(0, 3)
        gif_data=gif_dataa[escolha]
        id=gif_data["id"]
        url = "https://media.giphy.com/media/"+id+"/giphy.gif"
        await self.bot.say(embed=discord.Embed().set_image(url=url))

    #YOUTUBE
    @commands.command(pass_context=True, aliases=['yt', 'vid', 'video'])
    async def youtube(self, ctx, *, search:str):
        """Envia o primeiro resultado da pesquisa no youtube !youtube <pesquisa>."""
        response = requests.get(f"https://www.youtube.com/results?search_query={search}").text
        result = BeautifulSoup(response, "lxml")
        dir_address = f"{result.find_all(attrs={'class': 'yt-uix-tile-link'})[0].get('href')}"
        output=f"https://www.youtube.com{dir_address}"
        await self.bot.delete_message(ctx.message)
        await self.bot.say(output)


def setup(bot):
    bot.add_cog(Midia(bot))