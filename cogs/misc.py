import discord
import random
import secrets
import string
import re   
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands

class Misc:
    def __init__(self, bot):
        self.bot = bot
    
    #DIZ
    @commands.command(pass_context=True)
    async def diz(self, ctx, *, msg: str):
        """Repete uma mensagem /diz"""
        msg = re.sub('´', '`', msg)
        await self.bot.say(msg)
    @diz.error
    async def diz_error(self, ctx, error):
        if Exception == 'BadArgument':
            await self.bot.say('Utilize o comando corretamente digitando ```!diz <"mensagem a ser dita">```')

    #REPETE
    @commands.command()
    async def repete(self, x : int,* , content='repetindo...'):
        """Repete uma mensagem x vezes /repete x msg."""
        for i in range(x):
            await asyncio.sleep(1)
            await self.bot.say(content)

    #SENHA
    @commands.command(pass_context=True)
    async def senha(self, ctx, N=8):
        """Gera uma senha de acordo com a quantidade de caracteres solicitada !senha <quantidade>."""
        senha = await Misc.randomsenha(N)
        await self.bot.say(senha)
#    @senha.error
#    async def senha_error(self, ctx, error):
#        await self.bot.say('Utilize o comando corretamente digitando ```!senha <numero de caracteres>```')

    #PING        
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Responde com Pong e a latencia."""
        d = datetime.utcnow() - ctx.message.timestamp
        s = d.seconds * 1000 + d.microseconds // 1000
        await self.bot.say(":ping_pong: Pong! com {}ms".format(s))

    #CONVITE
    @commands.command()
    async def convite(self):
        """Envia um convite do servidor."""
        await self.bot.say('discord.gg/SyBkxmR')
    
    #DONATE
    @commands.command()
    async def donate(self):
        """Envia links que te permitem contruibuir com o bot."""
        await self.bot.say('https://u.muxy.io/tip/tmpoarr')    

    async def randomsenha(N:int):
        randomsenha : str
        randomsenha = ''
        randomsenha = randomsenha.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(N))
        return randomsenha

def setup(bot):
    bot.add_cog(Misc(bot))