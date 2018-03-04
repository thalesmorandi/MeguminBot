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
from utils import user_bd
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

cogs_dir = "cogs"
codigofile = open("codigo/codigo.txt", "r")
codigo=codigofile.read()
canal_codigo = '417822182379356190'
canal_logbv = '416924036048617473'
cargo_membro = 'Membro'

#=================================================FUNÇÕES=================================================#

async def attcodigo():
	server = list(bot.servers)[0]
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
	tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
	server = member.server
	canal = discord.utils.get(server.channels, name="membrosnovos")
	await bot.send_message(canal, '{0.mention} entrou aqui no dia {1}'.format(member, tempo))
	await bot.send_message(member, 'Bem Vindo ao '+ member.server.name + ' ' + member.mention + '\nLeias as regras para ter acesso completo ao servidor.')

#=================================================CODIGOS=================================================#

@bot.event
async def on_message(message):
	if message.content.startswith(codigo) and message.channel.id == canal_codigo:
		cargomembro = discord.utils.find(lambda r: r.name == cargo_membro, message.server.roles)
		await attcodigo()
		await bot.add_roles(message.author, cargomembro)

	if not message.content.startswith('!') and not message.channel == canal_codigo:
		usuario = message.author
		server = message.server
		xpganha = random.randint(1, 3)
		await user_bd.set_xp(usuario.id, xpganha)
		usuario_level = await user_bd.get_level(usuario.id)
		usuario_xp = await user_bd.get_xp(usuario.id)
		if usuario_level == 0:
			await user_bd.set_level(usuario.id, 1)
			await user_bd.set_eris(usuario.id, 10)
		upxp = (usuario_level * usuario_level)*10
		if usuario_xp >= upxp:
			await user_bd.set_level(usuario.id, 1)
			await user_bd.set_eris(usuario.id, 10)
				
		await user_bd.set_local_xp(server.id, usuario.id, xpganha)
		usuario_level = await user_bd.get_local_level(server.id, usuario.id)
		usuario_xp = await user_bd.get_local_xp(server.id, usuario.id)
		if usuario_level == 0:
			await user_bd.set_local_level(server.id, usuario.id, 1)
		upxp = (usuario_level * usuario_level)*10
		if usuario_xp >= upxp:
			await user_bd.set_local_level(server.id, usuario.id, 1)
			embed = discord.Embed(color=0x06ff2c)
			embed.set_thumbnail(url=usuario.avatar_url)
			embed.add_field(name=usuario.name, value='Upou para o **level {}**!'.format(usuario_level+1), inline=False)
			embed.add_field(name='Ganhou', value='**10** Eris.' )
			await bot.send_message(message.channel, embed=embed)

	if message.author.id == "397606105594986499" and not message.content.startswith('!'):
		await bot.add_reaction(message, '🇹')
		await bot.add_reaction(message, '🇪')
		await bot.add_reaction(message, '💖')
		await bot.add_reaction(message, '🇦')
		await bot.add_reaction(message, '🇲')
		await bot.add_reaction(message, '🇴')
	
	await bot.process_commands(message)


if __name__ == "__main__":
	for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
		try:
			bot.load_extension(cogs_dir + "." + extension)
			print(f'{extension} carregada com sucesso.')
		except Exception as e:
			print(f'erro ao carregar {extension}.')
			traceback.print_exc()


bot.run(token)