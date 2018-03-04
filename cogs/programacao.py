import discord
import re
from discord.ext import commands

class Programacao():
    def __init__(self, bot):
        self.bot = bot

    #JSON
    @commands.command(pass_context=True)
    async def json(self, ctx, *, code:str):
        """Auto formatação de codigo para JSON."""
        code = re.sub('`', '´', code)
        await self.bot.delete_message(ctx.message)
        await self.bot.say('**{0} enviou o seguinte codigo : **\n```json\n{1}\n```'.format(ctx.message.author.mention, code))
        await self.bot.say('**~> ` <~ (cráses)  são trocadas por  (agudo) ~> ´ <~**')
    @json.error
    async def json_error(self, ctx, error):
        await self.bot.say('Use o comando corretamente digitando !json <codigo>')

    #PY
    @commands.command(pass_context=True)
    async def py(self, ctx, *, code:str):
        """Auto formatação de codigo para Python."""
        code = re.sub('`', '´', code)
        await self.bot.delete_message(ctx.message)
        await self.bot.say('**{0} enviou o seguinte codigo : **\n```py\n{1}\n```'.format(ctx.message.author.mention, code))
        await self.bot.say('**~> ` <~ (cráses)  são trocadas por  (agudo) ~> ´ <~**')
    @py.error
    async def py_error(self, ctx, error):
        await self.bot.say('Use o comando corretamente digitando !py <codigo>')        


def setup(bot):
    bot.add_cog(Programacao(bot))