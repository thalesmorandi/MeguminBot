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
    async def diz(self, ctx, *, msg):
        """Repete uma mensagem /diz"""
        msg = re.sub('´', '`', msg)
        await self.bot.say(msg)

    #REPETE
    @commands.command()
    async def repete(self, x : int,* , content : str):
        """Repete uma mensagem x vezes /repete x msg."""
        for i in range(x):
            await asyncio.sleep(1)
            await self.bot.say(content)
    @repete.error
    async def repete_error(self, error, ctx):
        if isinstance(error, commands.BadArgument):
            await self.bot.say("use o comando digitando `!repete <numero de vezes a repetir> <msg a repetir>`")
        if isinstance(error, commands.MissingRequiredArgument):
            await self.bot.say("use o comando digitando `!repete <numero de vezes a repetir> <msg a repetir>`") 


    #SENHA
    @commands.command(pass_context=True)
    async def senha(self, ctx, N : int):
        """Gera uma senha de acordo com a quantidade de caracteres solicitada !senha <quantidade>."""
        if N<=2000 :
            senha = await Misc.randomsenha(N)
            await self.bot.say(senha)
        else:
            await self.bot.say("use o comando digitando `!senha <numero de caracteres até 2000>`") 
    @senha.error
    async def senha_error(self, error, ctx):
        if isinstance(error, commands.BadArgument):
            await self.bot.say("use o comando digitando `!senha <numero de caracteres até 2000>`")
        if isinstance(error, commands.MissingRequiredArgument):
            await self.bot.say("use o comando digitando `!senha <numero de caracteres até 2000>`") 



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

    #REPORTAR
    @commands.command(pass_context=True)
    async def reportar(self, ctx, *, report):
        """Envia um report de bug para o dono do bot"""
        member = discord.utils.get(self.bot.get_all_members(), id='182635477977923585')
        await self.bot.send_message(member,f'{ctx.message.author.mention} send : ' + report) 

    #DONATE
    @commands.command()
    async def donate(self):
        """Envia um link para que possa contruibuir com o bot."""
        await self.bot.say('https://u.muxy.io/tip/tmpoarr')    

    async def randomsenha(N:int):
        randomsenha : str
        randomsenha = ''
        randomsenha = randomsenha.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(N))
        return randomsenha

def setup(bot):
    bot.add_cog(Misc(bot))