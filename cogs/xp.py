import discord
from utils import user_bd
from discord.ext import commands
class xp():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def level(self, ctx, member: discord.Member = None):
        """Informa o level do membro ou seu."""
        if member is None:
            member = ctx.message.author       
        level = await user_bd.get_level(member.id)
        embedlevel = discord.Embed(title='{.name}'.format(member), description='É level : {}'.format(level))
        await self.bot.send_message(ctx.message.channel, embed=embedlevel)              

    @commands.command(pass_context=True)
    async def xp(self, ctx, member: discord.Member = None):
        """Informa a xp do membro ou sua."""
        if member is None:
            member = ctx.message.author
        await self.bot.send_message(ctx.message.channel, "O membro {} possui `{}` XP!".format(member.mention, await user_bd.get_xp(member.id)))

    @commands.command(pass_context=True)
    async def eris(self, ctx):
        """Informa o seu saldo de Eris."""
        eris = await user_bd.get_eris(ctx.message.author.id)
        embederis = discord.Embed(title='💠 Eris', description='{} tem {} Eris!'.format(ctx.message.author.name, eris))
        await self.bot.send_message(ctx.message.channel, embed=embederis)

    @commands.command(pass_context=True)
    async def enviar(self, ctx, qntdd: int,  member: discord.Member = None):
        """Envia uma quantia de Eris para outro membro."""
        if member == ctx.message.author:
            embedenviar = discord.Embed(title='💠 Transação sem sucesso', description='Doar só é um belo gesto, quando não pra sí mesmo')
            await self.bot.send_message(ctx.message.channel, embed=embedenviar)    
        else:
            user = ctx.message.author
            sendereris = await user_bd.get_eris(user.id)
            resto = sendereris - qntdd
            if resto >= 0:
                await user_bd.set_eris(user.id, -qntdd)
                await user_bd.set_eris(member.id, qntdd)
                embed2 = discord.Embed(title='💠 Transação', description='{} doou {} Eris para {}.'.format(user.name, qntdd, member.name))
                await self.bot.send_message(ctx.message.channel, embed=embed2)
            else:
                embedsemsaldo = discord.Embed(title='💠 Transação sem sucesso', description='Você não possui saldo suficiente para esta transação')
                await self.bot.send_message(ctx.message.channel, embed=embedsemsaldo) 

    @commands.command(pass_context=True, hidden=True)
    async def givexp(self, ctx, qntdd:int, member: discord.Member = None):
        if ctx.message.author.id == '182635477977923585':
            if qntdd > 0:
                if member is None: 
                    member = ctx.message.author
                user_bd.set_xp(member.id, qntdd)
                await self.bot.send_message(ctx.message.channel, "Adicionado `{1}` XP! para o membro {0}, nova quantia de XP é : `{2}`.".format(member.mention, qntdd, user_bd.get_xp(member.id)))
            else:
                await self.bot.send_message(ctx.message.channel, "A quantia deve ser positiva.")

        else:
            await self.bot.send_message(ctx.message.channel, 'Sem roubo de xp por hoje <:NicoSmug:416694328858116106>')

    @commands.command(pass_context=True, hidden=True)
    async def removexp(self, ctx, qntdd:int, member: discord.Member = None):
        if ctx.message.author.id == '182635477977923585':
            if qntdd > 0:
                if member is None: 
                    member = ctx.message.author
                user_bd.set_xp(member.id, qntdd)
                await self.bot.send_message(ctx.message.channel, "Removido `{1}` XP! do membro {0}, nova quantia de XP é : `{2}`.".format(member.mention, qntdd, user_bd.get_xp(member.id)))
            else:
                await self.bot.send_message(ctx.message.channel, "A quantia deve ser positiva.")            
        else:
            await self.bot.send_message(ctx.message.channel, 'Sem roubo de xp por hoje <:NicoSmug:416694328858116106>')
 
             
def setup(bot):
    bot.add_cog(xp(bot))