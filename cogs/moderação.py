import discord
import asyncio
from discord.ext import commands

class Moderacao:
    def __init__(self, bot):
        self.bot = bot

    #DELETE
    @commands.command(pass_context=True)
    async def delete(self, ctx, amount, channel: discord.Channel=None):
        """Deleta a quantidade de mensagens desejada !delete <quantidade>."""
        channel = channel or ctx.message.channel
        deleteds = 0
        total = amount
        try:
            amount = int(amount)
            await self.bot.delete_message(ctx.message)
            if amount > 100:
                amountdiv = int(amount/100)
                amountrest = amount-(amountdiv*100)
                for amount in range(amount, amountrest, -100):
                    deleted = await self.bot.purge_from(channel, limit=amount)
                    deleteds = deleteds + len(deleted)
            else:
                deleted = await self.bot.purge_from(channel, limit=amount)
                deleteds = deleteds + len(deleted)
        except ValueError:
            await self.bot.say('Utilize o comando com uma quantidade valida : ```!delete <quantidade>```')
        botmsgdelete = await self.bot.send_message(ctx.message.channel,'Deletei {} mensagens de um pedido de {} no canal {} para {}'.format(deleteds, total, channel.mention,ctx.message.author.mention))
        await asyncio.sleep(5)
        await self.bot.delete_message(botmsgdelete)

def setup(bot):
    bot.add_cog(Moderacao(bot))