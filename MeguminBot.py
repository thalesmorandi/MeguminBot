import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
#token imports
import config
#legal/moeda imports
import random
#getUser imports
import re
#cats imports
import aiohttp
import websockets
#ping imports
from datetime import datetime, timedelta



token = config.bottoken
bot = Bot(description="rsrs", command_prefix=commands.when_mentioned_or('!'), pm_help = False)
	
#função p pegar qualquer user pelo ID ou Name, necessita atrelar a var server pro server de pesquisa
def getUser(name, msg):
    server = msg.server
    if name == None:
        return None
    if name == '' or name == ' ':
        return None
    if re.search(r'\d{17,18}', name):
        name = re.search(r'\d{17,18}', name).group(0)
        print(name)
    for n in server.members:
        if re.search( name, n.name + n.discriminator, re.I) or re.search( name, n.display_name, re.I) or name == n.id:
            return n
    print('getUser invalid name or id')
    return None

#==================================================EVENTOS==================================================#
#BOT START
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
	print('Github Link: https://github.com/ThalesMorandi/Meguminbot')
	print('-------------------------------------------------------------------------------------------------')
	return await bot.change_presence(game=discord.Game(name='a raba pro alto'))


#MEMBRO NOVO
@bot.event
async def on_member_join(member):
    #Envia uma mensagem privada de boas vindas com o nome do servidor e mencionando o usuario
    await client.send_message(member, 'Bem Vindo ao '+ member.server.name + ' ' + member.mention)
    await client.send_message(bot.get_channel('416924036048617473'), ' '+ member.mention)
    #Adiciona o cargo "Membro" ao membro que entrou
    role = discord.utils.find(lambda r: r.name == "Membro", member.server.roles)
    await client.add_roles(member, role)	

#=================================================COMANDOS=================================================#

#APELIDO
@bot.command(pass_context=True)
async def apelido(ctx, nome=""):
	"""Altera o apelido para o desejado /apelido "novo apelido" (com aspas para apelidos com espaço)."""
	membro = ctx.message.author
	if nome == '' or nome == ' ': 
		await bot.say('Utilize o comando digitando ```!apelido <apelido novo>```')
	else: 
		if ctx.message.author.nick != None:
			apelidoold = ctx.message.author.nick
		else:
			apelidoold = ctx.message.author.name
		try:
			await bot.change_nickname(membro, nome)
			await bot.say('Alterando o apelido do membro : {0.mention} que era \'**'.format(membro)+apelidoold+'**\' para : \'** '+nome+' **\' ')
		except discord.errors.Forbidden:
			await bot.say('Não foi possivel realizar o pedido.')


#CAT
@bot.command(pass_context=True)
async def cat(ctx):
	"""Envia um catineo aleatorio."""	
	async with aiohttp.get('http://random.cat/meow') as r:
		if r.status == 200:
			js = await r.json()
			await bot.say(js['file'])


#CONVITE
@bot.command()
async def convite():
	"""Envia um convite do servidor."""
	await bot.say('discord.gg/V2WUn6M')
		

#DIZ
@bot.command()
async def diz(content):
	"""Repete uma mensagem /diz"""
	await bot.say(content)


#DOG
@bot.command(pass_context=True)
async def dog	(ctx):
	"""Envia um catiorineo aleatorio."""
	async with aiohttp.get('https://random.dog/woof.json') as r:
		if r.status == 200:
			js = await r.json()
			await bot.say(js['url'])	


#ENTROU
@bot.command(pass_context=True)
async def entrou(ctx, member: discord.Member = None):
	"""Informa quando você ou membro marcado entrou no servidor."""
	if member is None:
		member = ctx.message.author
	tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
	await bot.say('{0.mention} entrou aqui {1}'.format(member, tempo))


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


#REPETE
@bot.command()
async def repete(x : int, content='repetindo...'):
	"""Repete uma mensagem x vezes /repete x msg."""
	for i in range(x):
		await asyncio.sleep(1)
		await bot.say(content)

	
bot.run(token)