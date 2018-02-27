import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import botconfigs
import random
#cats imports
import aiohttp
import websockets
#ping imports
from datetime import datetime, timedelta

bot = Bot(description="uma cobaia muito obediente", command_prefix=commands.when_mentioned_or('!'), pm_help = False)

@bot.command(pass_context=True)
async def ola(ctx):
    await bot.say("Olá.")
    