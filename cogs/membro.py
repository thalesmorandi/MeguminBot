import discord
import random
import utils.chat_formatting
from discord.ext import commands
from utils import user_bd
from utils.chat_formatting import pagify

class Membro():
    def __init__(self, bot):
        self.bot = bot

    #APELIDO
    @commands.command(pass_context=True)
    async def apelido(self, ctx, *, nome: str = None):
        """Altera seu apelido para um desejado /apelido novo apelido."""
        membro = ctx.message.author
        if ctx.message.author.nick != None:
            apelidoold = ctx.message.author.nick
        else:
            apelidoold = ctx.message.author.name
        await self.bot.change_nickname(membro, nome)
        await self.bot.say('Alterando o apelido do membro : {0.mention} que era \'**'.format(membro)+apelidoold+'**\' para : \'** '+nome+' **\' ')
    @apelido.error
    async def apelido_error(self, ctx, error):
        await self.bot.say('Utilize o comando corretamente digitando ```!apelido apelido novo```')

    @commands.command(pass_context=True)
    async def perfil(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        """Exibe o seu perfil ou de um membro."""
        eris = await user_bd.get_eris(member.id)
        xpe = await user_bd.get_xp(member.id)
        level = await user_bd.get_level(member.id)
        barra = await user_bd.get_xpbar(member.id)
        exp = await user_bd.get_exp(member.id)        
        tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
        embedperfil = discord.Embed(title="Perfil do membro: " + member.name, color=0x46EEFF)
        if member.avatar_url == "":
            avatar_url='http://www.bool-tech.com/wp-content/uploads/bb-plugin/cache/WBBQ55TF_o-square.jpg'
        else:
            avatar_url = member.avatar_url
        embedperfil.set_thumbnail(url=avatar_url)
        embedperfil.add_field(name='Informação', value='Level: {0} ({1})\n{2}\nRank: #1 | XP Total : {3}\nReputação: 0'.format(level, exp, barra, xpe))
        embedperfil.add_field(name='Informação global', value='Level: {0} ({1})\n{2}\nRank: #1'.format(level, exp, barra))
        embedperfil.add_field(name='Eris', value='{} 💠'.format(eris))
        #if couple.name not is None:
            #embedperfil.add_field(name='Casado com', value='💕 {}'.format(couple.name))
        embedperfil.add_field(name='Comando favorito', value='help (18)')  
        embedperfil.add_field(name='Conquistas', value='Nenhuma (ainda!)')
        embedperfil.set_footer(text='membro desde '+ tempo +' | tempo de resposta: 150ms')
        await self.bot.send_message(ctx.message.channel, embed=embedperfil)

    @commands.command(pass_context=True)
    async def entrou(self, ctx, member: discord.Member = None):
        """Informa quando você ou membro marcado entrou no servidor."""
        if member is None:
            member = ctx.message.author
        tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
        await self.bot.say('{0.mention} entrou aqui no dia {1}'.format(member, tempo))

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
    bot.add_cog(Membro(bot))