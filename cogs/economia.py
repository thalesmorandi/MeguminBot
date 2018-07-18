import discord
import datetime
from utils import user_bd
from discord.ext import commands
class Economia():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def eris(self, ctx):
        """Informa o seu saldo de Eris."""
        eris = await user_bd.get_eris(ctx.message.author.id)
        embederis = discord.Embed(title='<:eris:420848536444207104> Eris', description='{} tem {} Eris!'.format(ctx.message.author.name, eris))
        await self.bot.send_message(ctx.message.channel, embed=embederis)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def diario(self, ctx):
        """Receba seus Eris diario."""
        eris = await user_bd.set_eris(ctx.message.author.id, 25)
        embeddiario = discord.Embed(title='<:eris:420848536444207104> Eris', description='Você recebeu 25 Eris!'.format(ctx.message.author.name, eris))
        await self.bot.send_message(ctx.message.channel, embed=embeddiario)
    @diario.error
    async def diario_error(self, error, ctx):
        if isinstance(error,commands.CommandOnCooldown):        
            embeddiario = discord.Embed(title='<:eris:420848536444207104> Eris', description='Você já pegou seus Eris diarios! Tente novamente em {}.'.format(str(datetime.timedelta(seconds=int(error.retry_after)))))
            await self.bot.say(embed=embeddiario)

    @commands.command(pass_context=True)
    async def natalmaiscedo(self, ctx, qntdd: int,  member: discord.Member = None):
        if ctx.message.author.id=="182635477977923585":
            await user_bd.set_eris(member.id, qntdd)
        else: 
            return

    @commands.command(pass_context=True)
    async def enviar(self, ctx, qntdd: int,  member: discord.Member = None):
        """Envia uma quantia de Eris para outro membro."""
        if member == ctx.message.author:
            embedenviar = discord.Embed(title='<:eris:420848536444207104> Transação sem sucesso', description='Doar só é um belo gesto, quando não pra sí mesmo')
            await self.bot.send_message(ctx.message.channel, embed=embedenviar)    
        elif qntdd > 0:
            user = ctx.message.author
            sendereris = await user_bd.get_eris(user.id)
            resto = sendereris - qntdd
            if resto >= 0:
                await user_bd.set_eris(user.id, -qntdd)
                await user_bd.set_eris(member.id, qntdd)
                embed2 = discord.Embed(title='<:eris:420848536444207104> Transação', description='{} doou {} Eris para {}.'.format(user.name, qntdd, member.name))
                await self.bot.send_message(ctx.message.channel, embed=embed2)
            else:
                embedsemsaldo = discord.Embed(title='<:eris:420848536444207104> Transação sem sucesso', description='Você não possui saldo suficiente para esta transação')
                await self.bot.send_message(ctx.message.channel, embed=embedsemsaldo)
        else:
            embedenviar = discord.Embed(title='<:eris:420848536444207104> Transação sem sucesso', description='Talvez isso funcione se você tentar enviar **ALGO** rs')
            await self.bot.send_message(ctx.message.channel, embed=embedenviar)               
 
             
def setup(bot):
    bot.add_cog(Economia(bot))