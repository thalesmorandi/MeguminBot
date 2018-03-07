import discord
from discord.ext import commands

class Geral:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def google(self, ctx, *, search_terms: str):
        """Faz uma pesquisa do google para vc pelo lgmtfy"""
        search_terms = search_terms.replace(" ", "+")
        await self.bot.say("https://lmgtfy.com/?q={}".format(search_terms))


    @commands.command(pass_context=True, guild_only=True)
    async def serverinfo(self, ctx):
        """Mostra informações sobre o servidor"""
        server = ctx.message.server
        verif = server.verification_level
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        if server.features == []:
            features = "None"
        else:
            features = str(server.features).replace("[", "").replace("]", "")
        embed = discord.Embed(color=0xDEADBF)
        embed.add_field(name="Nome", value=f"**{server.name}**\n({server.id})")
        embed.add_field(name="Dono", value=server.owner)
        embed.add_field(name="Membros online", value=f"**{online}/{len(server.members)}**")
        embed.add_field(name="Criado em ", value=server.created_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Canais ", value=f"**{len(server.channels)}**")
        embed.add_field(name="Cargos", value=len(server.roles))
        embed.add_field(name="Emojis", value=f"{len(server.emojis)}/100")
        embed.add_field(name="Região", value=str(server.region).title())
        embed.add_field(name="Segurança", value=f"Level de verificação: **{verif}**")
        try:
            embed.set_thumbnail(url=server.icon_url)
        except:
            pass
        await self.bot.say(embed=embed) 

    @commands.command(pass_context=True)
    async def votar(self, ctx):
        """Ajude o bot votando nele."""
        embed = discord.Embed(color=0xDEADBF,
                              title="Link de votação",
                              description="https://discordbots.org/bot/417982567699185665/vote")
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def qr(self, ctx, *, message: str):
        """Gera um QR code para uma mensagem ou link"""
        new_message = message.replace(" ", "+")
        url = f"http://api.qrserver.com/v1/create-qr-code/?data={new_message}"
        embed = discord.Embed(color=0xDEADBF)
        embed.set_image(url=url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, aliases=['comandos'])
    async def help(self, ctx, option: str = None):
        """Lista de comandos."""
        color = 0xDEADBF
        try:
            embed = discord.Embed(color=color,
                                  title=f"Prefixo: '!'")
            embed.set_author(name="MeguminBot",
                             icon_url="https://images.discordapp.net/avatars/332248296179630080/f634f3b13b3ce34b6b0d28649072209e.png?size=512")

            embed.add_field(name="Geral", value="`comandos`, `google`, `serverinfo`, `avatar`, `qr`, `votar`", inline=False)
            embed.add_field(name="Moderação", value="`renomear`, `kick`, `ban`, `mute`, `unmute`, `delete`", inline=False)
            embed.add_field(name="Membro", value="`avatar`, `apelido`, `perfil`, `rep`, `giverep`, `xp`, `level`", inline=False)
            embed.add_field(name="Diversão", value="`ship`, `isnowillegal`, `gif`, `cat`, `dog`, `legal`, `entrou`, `calcularamor`", inline=False)
            embed.add_field(name="Economia", value="`eris`, `enviar`, `diario`", inline=False)
            embed.add_field(name="Midia", value="`youtube`, `gif`", inline=False)
            embed.add_field(name="Jogos", value="`moeda`", inline=False)
            embed.add_field(name="Programação", value="`json`, `py`", inline=False)
            embed.add_field(name="Ações", value="`abraçar`, `beijar`, `carinho`, `socar`", inline=False)
            embed.add_field(name="Diversos", value="`senha`, `diz`, `repete`, `ping`, `donate`, `convite`, `reportar`", inline=False)
        except Exception as e:
            await self.bot.say(e)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def isnowillegal(self, ctx, legal : str):
        """Viro crime agoraa 11!UM!!ONZE!"""
        legal = legal.upper()
        url = "https://storage.googleapis.com/is-now-illegal.appspot.com/gifs/" + legal +".gif"
        em = discord.Embed(title="{} Viro crime!".format(legal))
        em.set_image(url=url)
        await self.bot.say(embed=em)


def setup(bot):
    bot.add_cog(Geral(bot))