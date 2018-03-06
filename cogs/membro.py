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

    @commands.command(pass_context=True, guild_only=True)
    async def avatar(self, ctx, member: discord.Member = None):
        """Exibe a sua ft de perfil ou de um membro"""
        if member is None:
            member = ctx.message.author
            if member.avatar_url == "":
                self.bot.say('Você não possui foto de perfil')
            else:
                await self.bot.say(embed=discord.Embed().set_image(url=member.avatar_url))
        else:
            if member.avatar_url == "":
                self.bot.say('{} não possui foto de perfil'.format(member.name))
            else:
                await self.bot.say(embed=discord.Embed().set_image(url=member.avatar_url))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)    
    async def perfil(self,  ctx, member: discord.Member = None):
        """Exibe o seu perfil ou de um membro."""
        if member is None:
            member = ctx.message.author
        if member.bot is False:
            server = ctx.message.server
            rep = await user_bd.get_rep(member.id)
            eris = await user_bd.get_eris(member.id)
            xpe = await user_bd.get_xp(member.id)
            level = await user_bd.get_level(member.id)
            barra = await user_bd.get_xpbar(member.id)
            exp = await user_bd.get_exp(member.id)        
            localxpe = await user_bd.get_local_xp(server.id, member.id)
            locallevel = await user_bd.get_local_level(server.id, member.id)
            localbarra = await user_bd.get_local_xpbar(server.id, member.id)
            localexp = await user_bd.get_local_exp(server.id, member.id)        
            tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
            embedperfil = discord.Embed(title="Perfil do membro: " + member.name, color=0x46EEFF)
            if member.avatar_url == "":
                avatar_url='http://www.bool-tech.com/wp-content/uploads/bb-plugin/cache/WBBQ55TF_o-square.jpg'
            else:
                avatar_url = member.avatar_url
            embedperfil.set_thumbnail(url=avatar_url)
            embedperfil.add_field(name='Informação', value='Level: {0} ({1})\n{2}\nRank: #1 | XP Total : {3}\nReputação: {4}'.format(locallevel, localexp, localbarra, localxpe, rep))
            embedperfil.add_field(name='Informação global', value='Level: {0} ({1})\n{2}\nRank: #1 | XP Total : {3}'.format(level, exp, barra, xpe))
            embedperfil.add_field(name='Eris', value='{} 💠'.format(eris))
            #if couple.name not is None:
                #embedperfil.add_field(name='Casado com', value='💕 {}'.format(couple.name))
            embedperfil.add_field(name='Comando favorito', value='help (18)')  
            embedperfil.add_field(name='Conquistas', value='Nenhuma (ainda!)')
            embedperfil.set_footer(text='membro desde '+ tempo +' | tempo de resposta: 150ms')
            await self.bot.send_message(ctx.message.channel, embed=embedperfil)

    @commands.command(pass_context=True)
    async def level(self, ctx, member: discord.Member = None):
        """Informa o level do membro ou seu."""
        if member is None:
            member = ctx.message.author       
        level = await user_bd.get_local_level(ctx.message.server.id, member.id)
        embedlevel = discord.Embed(title='{.name}'.format(member), description='É level : {}'.format(level))
        await self.bot.send_message(ctx.message.channel, embed=embedlevel)              

    @commands.command(pass_context=True)
    async def xp(self, ctx, member: discord.Member = None):
        """Informa a xp do membro ou sua."""
        if member is None:
            member = ctx.message.author
        xp = await user_bd.get_local_xp(ctx.message.server.id, member.id)
        embedxp = discord.Embed(title='{.name}'.format(member), description='Possui {} XP!'.format(xp))
        await self.bot.send_message(ctx.message.channel, embed=embedxp)

    @commands.command(pass_context=True)
    async def rep(self, ctx, member: discord.Member = None):
        """Informa a reputação do membro ou sua."""
        if member is None:
            member = ctx.message.author
        rep = await user_bd.get_rep(member.id)
        embedrep = discord.Embed(title='Reputação', description='{0.name} possui {1} pontos de reputação'.format(member, rep))
        await self.bot.send_message(ctx.message.channel, embed=embedrep)
    
    @commands.command(pass_context=True)
    @commands.cooldown(3, 86400, commands.BucketType.user)        
    async def giverep(self, ctx, member: discord.Member = None):
        """Envia pontos de reputação para um membro (limite de 3 a cada 24hrs.)"""
        if member == ctx.message.author: 
            embedrepaddself = discord.Embed(title='Reputação', description='Não é possivel conceder pontos de reputação a sí mesmo.')            
            await self.bot.send_message(ctx.message.channel, embed=embedrepaddself)
        else:
            await user_bd.set_rep(member.id, 1)
            embedrepadd = discord.Embed(title='Reputação', description='{0.name} concedeu 1 ponto de reputação à {1.name}'.format(ctx.message.author, member))
            await self.bot.send_message(ctx.message.channel, embed=embedrepadd)
    @giverep.error
    async def giverep_error(self, ctx, error):
        await self.bot.say('Você já enviou suas 3 reputações hoje.')

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