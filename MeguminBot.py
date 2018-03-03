import discord
import asyncio
import platform
import json
import io
import safygiphy
import bs4
import urllib.parse
import requests
import lxml
import random
import re
import aiohttp
import websockets
import secrets
import string
import os
import traceback
from os import listdir
from os.path import isfile, join
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen
from utils import functions, report, perms, rolechange

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
	token = os.environ.get('TOKEN')
else:
	import config
	token = config.bottoken
#=================================================**BOT**=================================================#

client = discord.Client()
bot = Bot(description="Uma maga disposta a fazer muitos truques por vc (づ｡◕‿‿◕｡)づ", command_prefix=commands.when_mentioned_or('!'), pm_help = False)

#=================================================VARIAVEIS=================================================#

msgcount = 0
cogs_dir = "cogs"
codigofile = open("codigo/codigo.txt", "r")
codigo=codigofile.read()
canal_codigo = '417822182379356190'
canal_logbv = '416924036048617473'
cargo_membro = 'Membro'
token = config.bottoken

#=================================================FUNÇÕES=================================================#

async def attcodigo():
	server = list(bot.servers)[0]
	channelcodigo=discord.utils.get(server.channels, name="regras")	
	msgcode = await bot.get_message(channel=discord.utils.get(server.channels, name="regras"), id="418680566183886848")
	N = random.randint(8, 12)	
	global codigo
	codigo = await randomstring(N)
	await bot.edit_message(msgcode, '**Coloque o codigo abaixo em #codigo para ter seu cargo de membro e poder usar o resto do nosso servidor:** \n codigo = ``'+ codigo +'``')
	await salvarcode()


async def salvarcode():
	codigoarq = open('codigo/codigo.txt', 'w')
	codigoarq.write(codigo)


async def randomstring(N:int):
	if N == None:
		N = 8
	randomstring : str
	randomstring = ''
	randomstring = randomstring.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(N))
	return randomstring


#==================================================EVENTOS==================================================#


@bot.event
async def on_ready():
	print('Logada como '+bot.user.name+' (ID:'+bot.user.id+') | Conectada a '+str(len(bot.servers))+' seridores | Em contato com '+str(len(set(bot.get_all_members())))+' usuarios')
	print('-------------------------------------------------------------------------------------------------')
	print('Versão do Discord.py : {} | Versão do Python : {}'.format(discord.__version__, platform.python_version()))
	print('-------------------------------------------------------------------------------------------------')
	print('Link de convite da {}:'.format(bot.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
	print('-------------------------------------------------------------------------------------------------')
	print('Servidor Discord : https://discord.me/discordialol')
	print('Github Link: https://github.com/ThalesMorandi/MeguminBot')
	print('-------------------------------------------------------------------------------------------------')
	print(is_prod)
	await attcodigo()
	return await bot.change_presence(game=discord.Game(name='a raba pro alto'))
	

@bot.event
async def on_member_join(member):
	await bot.send_message(member, 'Bem Vindo ao '+ member.server.name + ' ' + member.mention + '\nLeias as regras para ter acesso completo ao servidor.')
	cargo = discord.utils.find(lambda r: r.name == cargo_indigente, member.server.roles)
	await bot.add_roles(member, cargo)
	global canal_logbv
	canal_logbv = discord.utils.find(lambda r: r.id == canal_logbv, member.server.channels)
	tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
	await bot.send_message(canal_logbv, '{0.mention} entrou aqui no dia {1}'.format(member, tempo))
	
#=================================================CODIGOS=================================================#


@bot.event
async def on_message(message):
	if message.content.startswith(codigo) and message.channel.id == canal_codigo:
		cargomembro = discord.utils.find(lambda r: r.name == cargo_membro, message.server.roles)
		await attcodigo()
		await bot.add_roles(message.author, cargomembro)


	if message.author.id == "397606105594986499" and not message.content.startswith('!'):
		await bot.add_reaction(message, '🇹')
		await bot.add_reaction(message, '🇪')
		await bot.add_reaction(message, '💖')
		await bot.add_reaction(message, '🇦')
		await bot.add_reaction(message, '🇲')
		await bot.add_reaction(message, '🇴')
	global msgcount
	msgcount +=1
	
	await bot.process_commands(message)


#=================================================COMANDOS=================================================#

#CONVITE
@bot.command()
async def convite():
	"""Envia um convite do servidor."""
	await bot.say('discord.gg/V2WUn6M')
	print(msgcode)

#DELETE
@bot.command(pass_context=True)
async def delete(ctx, amount, channel: discord.Channel=None):
	"""Deleta a quantidade de mensagens desejada !delete <quantidade>."""
	channel = channel or ctx.message.channel
	deleteds = 0
	total = amount
	try:
		amount = int(amount)
		await bot.delete_message(ctx.message)
		if amount > 100:
			amountdiv = int(amount/100)
			amountrest = amount-(amountdiv*100)
			for amount in range(amount, amountrest, -100):
				deleted = await bot.purge_from(channel, limit=amount)
				deleteds = deleteds + len(deleted)
		else:
			deleted = await bot.purge_from(channel, limit=amount)
			deleteds = deleteds + len(deleted)
	except ValueError:
		await bot.say('Utilize o comando com uma quantidade valida : ```!delete <quantidade>```')
	botmsgdelete = await bot.send_message(ctx.message.channel,'Deletei {} mensagens de um pedido de {} no canal {} para {}'.format(deleteds, total, channel.mention,ctx.message.author.mention))
	await asyncio.sleep(5)
	await bot.delete_message(botmsgdelete)


#DIZ
@bot.command(pass_context=True)
async def diz(ctx, *, msg: str):
	"""Repete uma mensagem /diz"""
	msg = re.sub('´', '`', msg)
	await bot.say(msg)
@diz.error
async def diz_error(ctx, error):
	if Exception == 'BadArgument':
		await bot.say('Utilize o comando corretamente digitando ```!diz <"mensagem a ser dita">```')


#LEGAL
@bot.command(pass_context=True)
async def legal(ctx, member: discord.Member = None):
	"""Informa se você ou o membro marcado é legal"""
	if member is None:
		member = ctx.message.author
	result = random.randint(1, 2)
	if result == 1:
		await bot.say('Não, {0.mention} não é legal.'.format(member))
	if result == 2:	
		await bot.say('Sim, {0.mention} é legal.'.format(member))


#PING		
@bot.command(pass_context=True)
async def ping(ctx):
	"""Responde com Pong e a latencia."""

	d = datetime.utcnow() - ctx.message.timestamp
	s = d.seconds * 1000 + d.microseconds // 1000
	await bot.say(":ping_pong: Pong! com {}ms".format(s))


#REPETE
@bot.command()
async def repete(x : int,* , content='repetindo...'):
	"""Repete uma mensagem x vezes /repete x msg."""
	for i in range(x):
		await asyncio.sleep(1)
		await bot.say(content)


#SENHA
@bot.command(pass_context=True)
async def senha(ctx, N:int):
	"""Gera uma senha de acordo com a quantidade de caracteres solicitada !senha <quantidade>."""
	codigos = await randomstring(N)
	await bot.say(codigos)
@senha.error
async def senha_error(ctx, error):
	await bot.say('Utilize o comando corretamente digitando ```!senha <numero de caracteres>```')


if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            print(f'{extension} carregada com sucesso.')
        except Exception as e:
            print(f'erro ao carregar {extension}.')
            traceback.print_exc()


bot.run(token)