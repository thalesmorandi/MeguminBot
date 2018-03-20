import discord
import random
import utils.chat_formatting
from discord.ext import commands
from utils.chat_formatting import pagify


class Baixarias:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def penis(self, ctx, *users: discord.Member):
        """RSRS"""
        if not users:
            await self.bot.send_cmd_help(ctx)
            return

        dongs = {}
        msg = ""
        state = random.getstate()

        for user in users:
            random.seed(user.id)
            dongs[user] = "8{}D".format("=" * random.randint(0, 30))

        random.setstate(state)
        dongs = sorted(dongs.items(), key=lambda x: x[1])

        for user, dong in dongs:
            msg += "**Pinto do {} :**\n{}\n".format(user.display_name, dong)

        for page in pagify(msg):
            await self.bot.say(page)


def setup(bot):
    bot.add_cog(Baixarias(bot))