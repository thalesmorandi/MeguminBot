import discord
import random
import random
import secrets
import string
from discord.ext import commands
from utils import server_bd
class Codemod:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ativarcodigo(self, ctx, canalcodigo : discord.Channel, canalregras : discord.Channel, cargomembro : discord.Role):
        if ctx.message.author == ctx.message.server.owner:
            server_id = ctx.message.server.id
            resultado = await server_bd.get_server_codigo_status(server_id)
            if(resultado == 1):
                codigo = ""
                codigo = codigo.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                msgcodigo = await self.bot.send_message(canalregras, '**Coloque o codigo abaixo em {} para ter seu cargo {} e poder usar o resto do nosso servidor:** \ncodigo = ``{}``'.format(canalcodigo.mention, cargomembro.mention, codigo))
                await server_bd.codigo_setup(server_id, codigo, canalcodigo.id, canalregras.id, cargomembro.id, msgcodigo.id)
            else:
                self.bot.say("O bot já possui o serviço de codigo ativado.")
            #gerenciamento de permissões do codigo
            everyone = ctx.message.server.default_role
            overwrite = discord.PermissionOverwrite()
            for channel in ctx.message.server.channels:
                overwrite.read_messages = False
                overwrite.send_messages = False
                await self.bot.edit_channel_permissions(channel, everyone, overwrite) 
                overwrite.read_messages = True
                overwrite.send_messages = True
                await self.bot.edit_channel_permissions(channel, cargomembro, overwrite)               
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            await self.bot.edit_channel_permissions(canalcodigo, cargomembro, overwrite)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = True
            overwrite.manage_messages = False
            overwrite.read_message_history = False
            everyone = ctx.message.server.default_role
            await self.bot.edit_channel_permissions(canalcodigo, everyone, overwrite)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.send_messages = False
            overwrite.read_message_history = True
            await self.bot.edit_channel_permissions(canalregras, everyone, overwrite)
    @ativarcodigo.error
    async def ativarcodigo_error(self, error, ctx):
        if isinstance(error, commands.BadArgument):
            await self.bot.say("use o comando digitando `!ativarcodigo #canalcodigo #canalregras @cargomembro`")
        if isinstance(error, commands.MissingRequiredArgument):
            await self.bot.say("use o comando digitando `!ativarcodigo #canalcodigo #canalregras @cargomembro`")

    @commands.command(pass_context=True)
    async def debugcode(self, ctx):
        return

        



def setup(bot):
    bot.add_cog(Codemod(bot))