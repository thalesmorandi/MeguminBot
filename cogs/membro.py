import discord
import random
import datetime
import utils.chat_formatting
from discord.ext import commands
from utils import user_bd
from utils import chat_formatting
from utils.chat_formatting import pagify
from datetime import datetime, timedelta
import datetime
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
    @commands.cooldown(2, 10, commands.BucketType.user)    
    async def perfil(self,  ctx, member: discord.Member = None):
        """Exibe o seu perfil ou de um membro."""
        if member is None:
            member = ctx.message.author
        if member.bot is False:
            d = datetime.datetime.utcnow() - ctx.message.timestamp
            ping = d.seconds * 1000 + d.microseconds // 1000    
            server = ctx.message.server
            rep = await user_bd.get_rep(member.id)
            localrep = await user_bd.get_local_rep(member.id, server.id)
            eris = await user_bd.get_eris(member.id)
            xpe = await user_bd.get_xp(member.id)
            level = await user_bd.get_level(xpe)
            barra = await user_bd.get_xpbar(member.id)
            exp = await user_bd.get_exp(member.id)    
            bio = await user_bd.get_bio(member.id)   
            posrank = await user_bd.get_ranking_pos(member.id)
            posranklocal = await user_bd.get_local_ranking_pos(server.id, member.id)           
            localxpe = await user_bd.get_local_xp(server.id, member.id)
            locallevel = await user_bd.get_local_level(localxpe)
            localbarra = await user_bd.get_local_xpbar(server.id, member.id)
            couple = await  user_bd.get_couple(member.id)
            localexp = await user_bd.get_local_exp(server.id, member.id)        
            tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
            embedperfil = discord.Embed(title="Nome : "+member.name, color=0x46EEFF)
            if member.avatar_url == "":
                avatar_url='http://www.bool-tech.com/wp-content/uploads/bb-plugin/cache/WBBQ55TF_o-square.jpg'
            else:
                avatar_url = member.avatar_url
            embedperfil.set_thumbnail(url=avatar_url)
            embedperfil.add_field(name='Informação', value='Level: {0} ({1})\n{2}\nRank: #{5} | XP Total : {3}\nReputação: {4}'.format(locallevel, localexp, localbarra, localxpe, rep, posranklocal))
            embedperfil.add_field(name='Informação global', value='Level: {0} ({1})\n{2}\nRank: #{5} | XP Total : {3}\nReputação: {4}'.format(level, exp, barra, xpe, localrep, posrank))
            embedperfil.add_field(name='Bio', value=bio)  
            if couple is not None:
                couple = discord.utils.get(self.bot.get_all_members(), id=str(couple))
                embedperfil.add_field(name='Casado com', value='💕 {}'.format(couple.name))
            embedperfil.add_field(name='Eris', value='<:eris:420848536444207104> {}'.format(eris))
            embedperfil.add_field(name='Conquistas', value='Nenhuma (ainda!)')
            embedperfil.set_footer(text='membro desde '+ tempo +' | tempo de resposta: {}ms'.format(ping))
            await self.bot.send_message(ctx.message.channel, embed=embedperfil)

    @commands.command(pass_context=True)
    async def level(self, ctx, member: discord.Member = None):
        """Informa o level do membro ou seu."""
        if member is None:
            member = ctx.message.author       
        level = await user_bd.get_local_level(await user_bd.get_local_xp(ctx.message.server.id, member.id))
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
    async def casar(self, ctx, couple: discord.Member = None):
        """Pede um usuario em casamento."""
        msgpedido = ctx.message
        statusmember = await user_bd.get_couple(ctx.message.author.id)      
        if ctx.message.author != couple and couple != self.bot.user:
            if statusmember is None:
                statuscouple = await user_bd.get_couple(couple.id)
                if statuscouple is None:
                    embedcasados = discord.Embed(title='💌 Pedido de  casamento', description='{1} pediu {0} em casamento e cabe a ele(a) a decisão!'.format(couple.name, msgpedido.author.name))
                    msgcasar = await self.bot.send_message(msgpedido.channel, embed=embedcasados)                    
                    msgcasar_id = msgcasar.id
                    await self.bot.add_reaction(msgcasar, ":yep:422255563121098754")
                    await self.bot.add_reaction(msgcasar, ":nope:422255563099865110")
                    @self.bot.event
                    async def on_reaction_add(reaction, user):
                        emoji = str(reaction.emoji)
                        msg = reaction.message
                        if emoji == '<:yep:422255563121098754>' and msg.id == msgcasar_id and user.id == couple.id:
                            await user_bd.set_couple(ctx.message.author.id, couple.id)
                            await self.bot.delete_message(msgcasar)
                            embedcasados = discord.Embed(title='💒 Casamento', description='{} aceitou o pedido de {} e estão casados para sempre ~~ou não~~ 💞 !!'.format(couple.name, msgpedido.author.name))
                            await self.bot.send_message(msgpedido.channel, embed=embedcasados)
                        elif emoji == '<:nope:422255563099865110>' and msg.id == msgcasar_id and user.id == couple.id:
                            await self.bot.delete_message(msgcasar)
                            embedcasados = discord.Embed(title='💒 Casamento', description='{} recusou o pedido de {} 💔💔 '.format(couple.name, msgpedido.author.name))
                            await self.bot.send_message(msgpedido.channel, embed=embedcasados)
                        return
        elif ctx.message.author == couple and statusmember is None:
            embedcasados = discord.Embed(title='💒 Casamento', description='{} não se preocupe, logo logo você encontrará sua alma gêmea!'.format(ctx.message.author.name))
            await self.bot.send_message(msgpedido.channel, embed=embedcasados)
        elif couple == self.bot.user and statusmember is None:
            embedcasados = discord.Embed(title='💒 Casamento', description='{} robôs ainda não podem se casar 😭😭'.format(ctx.message.author.name))
            await self.bot.send_message(msgpedido.channel, embed=embedcasados)
        elif str(statusmember) != couple.id:
            embedcasados = discord.Embed(title='💒 Casamento', description='{} você já esta casado seu infieeel'.format(ctx.message.author.name))
            await self.bot.send_message(msgpedido.channel, embed=embedcasados)
    @commands.group(pass_context=True)
    async def ranking(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Especifique entre local e geral')


    @ranking.command(pass_context=True)
    async def local(self, ctx):
        ranking = await user_bd.get_local_ranking(ctx.message.server.id)
        embedranking = discord.Embed(title="Ranking Local", color=0x46EEFF)
        embedranking.set_author(name="MeguminBot Ranking", icon_url="https://images.discordapp.net/avatars/332248296179630080/f634f3b13b3ce34b6b0d28649072209e.png?size=512")    
        embedranking.set_thumbnail(url="https://cdn3.iconfinder.com/data/icons/unigrid-phantom-achievements-badges/60/028_021_achievement_badge_wreath_award_prize_top_rank_winner_win_cup-512.png")

        for _ in range(0, 10):
            try:
                rankingmember = ranking[_]
                memberid = rankingmember['memberid']
                memberxp = rankingmember['localxp']
                memberpos = _+1
                level = await user_bd.get_level(memberxp)
                membro = discord.utils.get(self.bot.get_all_members(), id=str(memberid))
                if memberpos == 1:
                    embedranking.add_field(name='**🥇 #1 **', value='{}#{}'.format(membro.name, membro.discriminator)) 
                    embedranking.add_field(name='💮 Level {}'.format(level), value='{} Exp'.format(memberxp))   
                elif memberpos == 2:
                    embedranking.add_field(name='**🥈 #2 **', value='{}#{}'.format(membro.name, membro.discriminator)) 
                    embedranking.add_field(name='💮 Level {}'.format(level), value='{} Exp'.format(memberxp))                  
                elif memberpos == 3:
                    embedranking.add_field(name='**🥉 #3 **', value='{}#{}'.format(membro.name, membro.discriminator)) 
                    embedranking.add_field(name='💮 Level {}'.format(level), value='{} Exp'.format(memberxp))  
                else:
                    embedranking.add_field(name='**🏅 #{} **'.format(memberpos), value='{}#{}'.format(membro.name, membro.discriminator)) 
                    embedranking.add_field(name='💮 Level {}'.format(level), value='{} Exp'.format(memberxp))              
            except:
                print('')
        await self.bot.send_message(ctx.message.channel, embed=embedranking)

    @ranking.command(pass_context=True)
    async def geral(self, ctx):
        ranking = await user_bd.get_ranking()
        embedranking = discord.Embed(title="Ranking Global", color=0x46EEFF)
        embedranking.set_author(name="MeguminBot Ranking", icon_url="https://images.discordapp.net/avatars/332248296179630080/f634f3b13b3ce34b6b0d28649072209e.png?size=512")    
        embedranking.set_thumbnail(url="https://cdn3.iconfinder.com/data/icons/unigrid-phantom-achievements-badges/60/028_021_achievement_badge_wreath_award_prize_top_rank_winner_win_cup-512.png")

        for _ in range(0, 10):
            try:
                rankingmember = ranking[_]
                memberid = rankingmember['id']
                memberxp = rankingmember['xp']
                memberpos = _+1
                level = await user_bd.get_level(memberxp)
                membro = discord.utils.get(self.bot.get_all_members(), id=str(memberid))
                if memberpos == 1:
                    embedranking.add_field(name='**🥇 #1 **', value='{}#{}'.format(membro.name, membro.discriminator)) 
                    embedranking.add_field(name='💮 Level {}'.format(level), value='{} Exp'.format(memberxp))   
                elif memberpos == 2:
                    embedranking.add_field(name='**🥈 #2 **', value='{}#{}'.format(membro.name, membro.discriminator)) 
                    embedranking.add_field(name='💮 Level {}'.format(level), value='{} Exp'.format(memberxp))                  
                elif memberpos == 3:
                    embedranking.add_field(name='**🥉 #3 **', value='{}#{}'.format(membro.name, membro.discriminator)) 
                    embedranking.add_field(name='💮 Level {}'.format(level), value='{} Exp'.format(memberxp))  
                else:
                    embedranking.add_field(name='**🏅 #{} **'.format(memberpos), value='{}#{}'.format(membro.name, membro.discriminator)) 
                    embedranking.add_field(name='💮 Level {}'.format(level), value='{} Exp'.format(memberxp))              
            except:
                print('')
        await self.bot.send_message(ctx.message.channel, embed=embedranking)

    @commands.command(pass_context=True)
    async def divorciar(self, ctx):
        """Se divorcia do seu atual conjuge."""
        statusmember = await user_bd.get_couple(ctx.message.author.id)
        if statusmember is not None:
            await user_bd.unset_couple(ctx.message.author.id, statusmember)
            couple = discord.utils.get(self.bot.get_all_members(), id=str(statusmember))
            embeddivorcio = discord.Embed(title='💔 Divorcio', description='{} se divorciou de {} 😭😭'.format(ctx.message.author.name, couple.name))
            await self.bot.send_message(ctx.message.channel, embed=embeddivorcio)            

    @commands.command(pass_context=True)
    async def rep(self, ctx, member: discord.Member = None):
        """Informa a reputação do membro ou sua."""
        if member is None:
            member = ctx.message.author
        rep = await user_bd.get_rep(member.id)
        embedrep = discord.Embed(title='Reputação', description='{0.name} possui {1} pontos de reputação'.format(member, rep))
        await self.bot.send_message(ctx.message.channel, embed=embedrep)

    @commands.command(pass_context=True)
    async def bio(self, ctx, *, bio):
        """Altera a sua bio."""
        await user_bd.set_bio(ctx.message.author.id, bio)


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
    async def giverep_error(self, error, ctx):
        if isinstance(error,commands.CommandOnCooldown):        
            embedgiverep = discord.Embed(title='Rep', description="Você já usou seus 3 rep's diarios! Tente novamente em {}.".format(str(datetime.timedelta(seconds=int(error.retry_after)))))
            await self.bot.say(embed=embedgiverep)

    @commands.command(pass_context=True)
    async def entrou(self, ctx, member: discord.Member = None):
        """Informa quando você ou membro marcado entrou no servidor."""
        if member is None:
            member = ctx.message.author
        tempo = member.joined_at.strftime('%d/   ás %H:%M')
        await self.bot.say('{0.mention} entrou aqui no dia {1}'.format(member, tempo))
    

def setup(bot):
    bot.add_cog(Membro(bot))