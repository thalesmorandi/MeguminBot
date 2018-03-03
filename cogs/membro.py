import discord
from discord.ext import commands
from cogs import xp
class membro():
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
    async def entrou(self, ctx, member: discord.Member = None):
        """Informa quando você ou membro marcado entrou no servidor."""
        if member is None:
            member = ctx.message.author
        tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
        await self.bot.say('{0.mention} entrou aqui no dia {1}'.format(member, tempo))






def setup(bot):
    bot.add_cog(membro(bot))