import discord
import random
import re
from utils import user_bd
from discord.ext import commands

class Jogos:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def moeda(self, ctx, lado, aposta: int):
        """Jogar apostando."""
        for f in re.findall("([A-Z]+)", lado):
            lado = lado.replace(f, f.lower())
        if lado == "cara" or "coroa":
            user = ctx.message.author
            sendereris = await user_bd.get_eris(user.id)
            resto = sendereris - aposta
            if resto >= 0:
                embed2 = discord.Embed(title='<:eris:420848536444207104> {} Apostou {} Eris em {}.'.format(user.name, aposta, lado), description='E a moeda caiu na posição...............')
                await self.bot.send_message(ctx.message.channel, embed=embed2)
                escolha = random.randint(1,2)
                if escolha == 1:
                    ladoc = "cara"
                    embed1=discord.Embed(title="{}".format(ladoc))
                    await self.bot.say(embed=embed1.set_image(url="https://i.imgur.com/nRC8gyk.png"))

                if escolha == 2:
                    ladoc = "coroa"
                    embed1=discord.Embed(title="A moeda caiu em {}".format(ladoc))
                    await self.bot.say(embed=embed1.set_image(url="https://i.imgur.com/j4cItvQ.png"))

                if lado == ladoc:
                    await user_bd.set_eris(user.id, aposta*0.5)
                else:    
                    await user_bd.set_eris(user.id, -aposta)
                    
            else:
                embedsemsaldo = discord.Embed(title='<:eris:420848536444207104> Aposta sem sucesso', description='Você não possui saldo suficiente para esta aposta')
                await self.bot.send_message(ctx.message.channel, embed=embedsemsaldo)
        else:
            return


def setup(bot):
    bot.add_cog(Jogos(bot))