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
import pickle
import os
from discord.ext.commands import Bot
from discord.ext import commands
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen
is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
	token = os.environ.get('TOKEN')
else:
	import config
	token = config.bottoken
#=================================================**BOT**=================================================#


bot = Bot(description="Uma maga disposta a fazer muitos truques por vc (づ｡◕‿‿◕｡)づ", command_prefix=commands.when_mentioned_or('!'), pm_help = False)


#=================================================VARIAVEIS=================================================#

myfile = open("codigo/codigo.txt", "r")
codigo=myfile.read()
msgcodeler = open('codigo/msgcodearq.p', 'rb')
msgcode = pickle.load(msgcodeler)
canal_codigo = '417822182379356190'
canal_logbv = '416924036048617473'
cargo_membro = 'Membro'
cargo_indigente = 'Indigente'
token = config.bottoken


#=================================================FUNÇÕES=================================================#


async def attcodigo():
	N = random.randint(8, 12)
	global msgcode
	global codigo
	codigo = await randomstring(N)
	msgcode = await bot.edit_message(msgcode, 'Coloque o codigo abaixo em #codigo para ter seu cargo de membro e poder usar o resto do nosso servidor: \n'+ codigo)
	await salvarcode()
	await salvarmsgcode()


async def salvarcode():
	codigoarq = open('codigo/codigo.txt', 'w')
	codigoarq.write(codigo)
async def salvarmsgcode():
	msgcodearq = open('codigo/msgcodearq.p', 'wb')
	pickle.dump(msgcode, msgcodearq)


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
	return await bot.change_presence(game=discord.Game(name='a raba pro alto'))
	

@bot.event
async def on_member_join(member):
	await bot.send_message(member, 'Bem Vindo ao '+ member.server.name + ' ' + member.mention + '\n Leias as regras para ter acesso completo ao servidor.')
	cargo = discord.utils.find(lambda r: r.name == cargo_indigente, member.server.roles)
	await bot.add_roles(member, cargo)
	
#=================================================CODIGOS=================================================#


@bot.event
async def on_message(message):
	if message.content.startswith(codigo) and message.channel.id == canal_codigo:
		cargomembro = discord.utils.find(lambda r: r.name == cargo_membro, message.server.roles)
		cargoindigente = discord.utils.find(lambda r: r.name == cargo_indigente, message.server.roles)
		await attcodigo()
		await bot.add_roles(message.author, cargomembro)
		await bot.remove_roles(message.author, cargoindigente)
	
	
	if message.author.id == "397606105594986499" and not message.content.startswith('!'):
		await bot.add_reaction(message, '🇹')
		await bot.add_reaction(message, '🇪')
		await bot.add_reaction(message, '💖')
		await bot.add_reaction(message, '🇦')
		await bot.add_reaction(message, '🇲')
		await bot.add_reaction(message, '🇴')
	
	await bot.process_commands(message)


#=================================================COMANDOS=================================================#

#APELIDO
@bot.command(pass_context=True)
async def apelido(ctx, *, nome: str = None):
	"""Altera seu apelido para um desejado /apelido novo apelido."""
	membro = ctx.message.author
	if ctx.message.author.nick != None:
		apelidoold = ctx.message.author.nick
	else:
		apelidoold = ctx.message.author.name
	await bot.change_nickname(membro, nome)
	await bot.say('Alterando o apelido do membro : {0.mention} que era \'**'.format(membro)+apelidoold+'**\' para : \'** '+nome+' **\' ')
@apelido.error
async def apelido_error(ctx, error):
	await bot.say('Utilize o comando corretamente digitando ```!apelido apelido novo```')


#CAT
@bot.command(pass_context=True)
async def cat(ctx):
	"""Envia um catineo aleatorio."""	
	async with aiohttp.ClientSession() as session:
		async with session.get('http://random.cat/meow') as r:
			if r.status == 200:
				js = await r.json()
				await bot.say(embed=discord.Embed().set_image(url=js['file']))


#CONVITE
@bot.command()
async def convite():
	"""Envia um convite do servidor."""
	await bot.say('discord.gg/V2WUn6M')

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
			print(amountdiv)
			print(amountrest)
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
@bot.command()
async def diz(*, msg: str):
	"""Repete uma mensagem /diz"""
	msg = re.sub('´', '`', msg)
	await bot.say(msg)
@diz.error
async def diz_error(error):
	#if isinstance(error, command.MissingRequiredArgument):
	await bot.say('Utilize o comando corretamente digitando ```!diz <"mensagem a ser dita">```')


#DOG
@bot.command(pass_context=True)
async def dog(ctx):
	"""Envia um catiorineo aleatorio."""
	async with aiohttp.ClientSession() as session:
		async with session.get('https://dog.ceo/api/breeds/image/random')	as r:	
			if r.status == 200:
				js = await r.json()
				await bot.say(embed=discord.Embed().set_image(url=js['message']))


#ENTROU
@bot.command(pass_context=True)
async def entrou(ctx, member: discord.Member = None):
	"""Informa quando você ou membro marcado entrou no servidor."""
	if member is None:
		member = ctx.message.author
	tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
	await bot.say('{0.mention} entrou aqui {1}'.format(member, tempo))


#GIF
@bot.command()
async def gif(*, stag:str):
	"""Envia um gif aleatorio com a tag escolhida !gif <tags>."""
	#msg = ctx.message.content
	#stag = re.sub('!gif ', '', msg)
	g = safygiphy.Giphy(token='rener21BaDh2WcIgmARoUpAZcDBAGaR3')
	r = g.search(q=stag, limit=25)
	gif_dataa=r['data']
	escolha = random.randint(0, 3)
	gif_data=gif_dataa[escolha]
	id=gif_data["id"]
	url = "https://media.giphy.com/media/"+id+"/giphy.gif"
	await bot.say(embed=discord.Embed().set_image(url=url))


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


#MOEDA
@bot.command(pass_context=True)
async def moeda(ctx):
	"""Irá sortear entre cara ou coroa."""
	message = ctx.message
	escolha = random.randint(1, 2)
	if escolha == 1:
		await bot.add_reaction(message, '😀')
	if escolha == 2:
		await bot.add_reaction(message, '👑')


#PING		
@bot.command(pass_context=True)
async def ping(ctx):
	"""Responde com Pong e a latencia."""

	d = datetime.utcnow() - ctx.message.timestamp
	s = d.seconds * 1000 + d.microseconds // 1000
	await bot.say(":ping_pong: Pong! com {}ms".format(s))


#PY
@bot.command(pass_context=True)
async def py(ctx, *, code:str):
	"""Auto formatação."""
	code = re.sub('`', '´', code)
	await bot.delete_message(ctx.message)
	await bot.say('**{0} Enviou o seguinte codigo : **\n```py\n{1}\n```'.format(ctx.message.author.mention, code))
	await bot.say('**~> ` <~ (CRÁSES)  são trocadas por  (AGUDO) ~> ´ <~**')
@py.error
async def py_error(ctx, error):
	await bot.say('Use o comando corretamente digitando !py <codigo>')

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
		

#YOUTUBE
@bot.command(aliases=['yt', 'vid', 'video'])
async def youtube(*, search:str):
	"""Envia o primeiro resultado da pesquisa no youtube !youtube <pesquisa>."""
	#search = re.sub('!yt ', '', ctx.message.content)
	#search = re.sub('!youtube ', '', search)
	#search = search.replace(' ', '+').lower()
	response = requests.get(f"https://www.youtube.com/results?search_query={search}").text
	result = BeautifulSoup(response, "lxml")
	dir_address = f"{result.find_all(attrs={'class': 'yt-uix-tile-link'})[0].get('href')}"
	output=f"https://www.youtube.com{dir_address}"
	await bot.say(output)

	
bot.run(token)