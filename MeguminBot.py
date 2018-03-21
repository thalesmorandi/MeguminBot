import discord
import asyncio
import platform
import io
import random
import secrets
import string
import traceback
import os
from os import listdir
from os.path import isfile, join
from discord.ext.commands import Bot
from discord.ext import commands
from utils import functions, report, perms, rolechange, server_bd, user_bd
is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
	token = os.environ.get('TOKEN')
else:
	import config
	token = config.bottoken

client = discord.Client()
bot = Bot(description="Uma maga disposta a fazer muitos truques por vc (づ｡◕‿‿◕｡)づ", command_prefix=commands.when_mentioned_or('!'), pm_help = False, help_attrs=dict(hidden=True, brief="Magicos não precisam de ajuda... ou precisam rs"))
bot.remove_command('help')
cogs_dir = "cogs"

	

@bot.event
async def on_ready():
	print('Logada como '+bot.user.name+' (ID:'+bot.user.id+') | Conectada a '+str(len(bot.servers))+' servidores | Em contato com '+str(len(set(bot.get_all_members())))+' usuarios')
	print('-------------------------------------------------------------------------------------------------')
	print('Versão do Discord.py : {} | Versão do Python : {}'.format(discord.__version__, platform.python_version()))
	print('-------------------------------------------------------------------------------------------------')
	print('Link de convite da {}:'.format(bot.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
	print('-------------------------------------------------------------------------------------------------')
	print('Servidor Discord : https://discord.me/discordialol')
	print('Github Link: https://github.com/ThalesMorandi/MeguminBot')
	print('-------------------------------------------------------------------------------------------------')
	return await bot.change_presence(game=discord.Game(name='caixas aleatoriamente'))

@bot.event
async def on_message(message):
	if not  message.channel.is_private:	
		codigo_ligado = await server_bd.get_server_codigo_ligado(message.server.id)
		if codigo_ligado == 1:
			canal_codigo = await server_bd.get_canal_codigo(message.server.id)
			canal_regras = await server_bd.get_canal_regras(message.server.id)	
			cargo_membro = await server_bd.get_cargo_membro(message.server.id)
			codigo = await server_bd.get_server_codigo(message.server.id)
			msgcode = await server_bd.get_msgcode(message.server.id)
			server = message.server
			if message.content == codigo and message.channel.id == str(canal_codigo):
				cargomembro = discord.utils.find(lambda r: r.id == str(cargo_membro), message.server.roles)
				codigo = ""
				codigo = codigo.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
				await server_bd.set_server_codigo(message.server.id, codigo)
				await bot.add_roles(message.author, cargomembro)
				channelcodigo=bot.get_channel(str(canal_codigo))
				channel=bot.get_channel(str(canal_regras))
				msgcode = await bot.get_message(channel, id=str(msgcode))
				await bot.edit_message(msgcode, '**Coloque o codigo abaixo em {} para ter seu cargo {} e poder usar o resto do nosso servidor:** \ncodigo = ``{}``'.format(channelcodigo.mention, cargomembro.mention, codigo))
			if message.content == "!debugcode" and message.author == message.server.owner:
				cargomembro = discord.utils.find(lambda r: r.id == str(cargo_membro), message.server.roles)				
				codigo = ""
				codigo = codigo.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
				await server_bd.set_server_codigo(message.server.id, codigo)
				channelcodigo=bot.get_channel(str(canal_codigo))
				channel=bot.get_channel(str(canal_regras))
				msgcode = await bot.get_message(channel, id=str(msgcode))
				await bot.edit_message(msgcode, '**Coloque o codigo abaixo em {} para ter seu cargo {} e poder usar o resto do nosso servidor:** \ncodigo = ``{}``'.format(channelcodigo.mention, cargomembro.mention, codigo))

		
		if not message.content.startswith('!') and not message.author.bot is True:
			usuario = message.author
			server = message.server
			xpganha = random.randint(1, 5)
			usuario_local_xp = await user_bd.get_local_xp(server.id, usuario.id)		
			usuario_local_level = await user_bd.get_local_level(usuario_local_xp)
			usuario_new_level = await user_bd.get_local_level(usuario_local_xp+xpganha)

			if usuario_local_level != usuario_new_level:
				embed = discord.Embed(color=0x06ff2c)
				embed.set_thumbnail(url=usuario.avatar_url)
				embed.add_field(name=usuario.name, value='Upou para o **level {}**!'.format(usuario_local_level+1), inline=False)
				embed.add_field(name='Ganhou', value='**100** Eris <:eris:420848536444207104>.' )
				await bot.send_message(message.channel, embed=embed)
				await user_bd.set_eris(usuario.id, 100)
			await user_bd.set_xp(usuario.id, xpganha)	
			await user_bd.set_local_xp(server.id, usuario.id, xpganha)		

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