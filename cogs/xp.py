import discord
import json
import os
import re
import random
from os import listdir
from os.path import isfile, join
from discord.ext import commands
class xp():
    def __init__(self, bot):
        self.bot = bot

    def user_add_xp(user_id: int, xp: int):
        if os.path.isfile("users.json"):
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id]['xp'] += xp
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
            except KeyError:
                try:
                    with open('users.json', 'r') as fp:
                        users = json.load(fp)
                    users[user_id]['xp'] = xp
                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)
                except KeyError:
                    with open('users.json', 'r') as fp:
                        users = json.load(fp)
                    users[user_id] = {}
                    users[user_id]['xp'] = xp
                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)                    
        else:
            users = {user_id: {}}
            users[user_id]['xp'] = xp
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    

    def get_xp(user_id: int):
        if os.path.isfile('users.json'):
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            return users[user_id]['xp']
        else:
            return 0
    

    def set_level(user_id: int, level: int):
        if os.path.isfile('users.json'):
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id]["level"] = level
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    

    def get_level(user_id: int):
        if os.path.isfile('users.json'):
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                return users[user_id]['level']
            except KeyError:        
                return 0


    def set_eris(user_id: int, eris: int):
        if os.path.isfile("users.json"):
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id]['eris'] += eris
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
            except KeyError:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id]['eris'] = eris
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
        else:
            users = {user_id: {}}
            users[user_id]['eris'] = eris
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)


    def get_eris(user_id: int):
        if os.path.isfile('users.json'):
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                return users[user_id]['eris']
            except KeyError:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id]['eris'] = 10
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)                
                return 10


    def get_exp(user_id:int):
        xpere = xp.get_xp(user_id)
        level = xp.get_level(user_id)
        if level > 1:
            levelcalc = level-1
            xpcalc = ((levelcalc*levelcalc)*10)
            xpatual = xpere - xpcalc
            xpcalc = ((level*level)*10)-xpcalc
            exp= str(str(xpatual)+'/'+str(xpcalc))
            return exp
        else:
            exp= str(xpere)+'/10'
            return exp       


    def get_xpbar(user_id:int):
        xpere = xp.get_xp(user_id)
        level = xp.get_level(user_id)
        if level > 1:
            levelcalc = level-1#1
            xpcalc = ((levelcalc*levelcalc)*10)#10
            xpatual = xpere - xpcalc #25
            xpcalc = ((level*level)*10)-xpcalc #30
            barrasverdes = int(xpatual/(xpcalc/6))
            barrasbrancas = 6 - barrasverdes
            if barrasbrancas==6:
                barra = '<:wbare:419367453613621249><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarr:419367453802627081>'             
            else:
                if barrasverdes==1:
                    barra = '<:gbare:419367453739450378><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarr:419367453802627081>'
                else:
                    if barrasverdes==2:
                        barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarr:419367453802627081>'
                    else:
                        if barrasverdes==3:
                            barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:gbarm:419367453609426945><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarr:419367453802627081>'
                        else:
                            if barrasverdes==4:
                                barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:wbarm:419367453475209217><:wbarr:419367453802627081>'
                            else:
                                if barrasverdes==5:
                                    barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:wbarr:419367453802627081>'
                                else:
                                    if barrasverdes==6:
                                        barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarr:419367453420683265>'
            return barra    
        else:
            levelcalc = level-1#1
            xpcalc = ((levelcalc*levelcalc)*10)#10
            xpatual = xpere - xpcalc #25
            xpcalc = ((level*level)*10)-xpcalc #30
            barrasverdes = int(xpatual/(xpcalc/6))
            barrasbrancas = 6 - barrasverdes
            print(barrasbrancas)
            print(barrasverdes)
            if barrasbrancas==6:
                barra = '<:wbare:419367453613621249><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarr:419367453802627081>'             
            else:
                if barrasverdes==1:
                    barra = '<:gbare:419367453739450378><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarr:419367453802627081>'
                else:
                    if barrasverdes==2:
                        barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarr:419367453802627081>'
                    else:
                        if barrasverdes==3:
                            barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:gbarm:419367453609426945><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarr:419367453802627081>'
                        else:
                            if barrasverdes==4:
                                barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:wbarm:419367453475209217><:wbarr:419367453802627081>'
                            else:
                                if barrasverdes==5:
                                    barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:wbarr:419367453802627081>'
                                else:
                                    if barrasverdes==6:
                                        barra = '<:gbare:419367453739450378><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarm:419367453609426945><:gbarr:419367453420683265>'
            return barra


    @commands.command(pass_context=True)
    async def level(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author       
        level = xp.get_level(member.id)
        await self.bot.say("{0.mention} é level {1}".format(member, level))   

    @commands.command(pass_context=True)
    async def enviar(self, ctx, qntdd: int,  member: discord.Member = None):
        if member == ctx.message.author:
            embed2 = discord.Embed(title='💠 transação sem sucesso', description='Doar só é um belo gesto, quando não pra sí mesmo')
            await self.bot.say(embed=embed2)    
        else:
            user = ctx.message.author
            sendereris = xp.get_eris(user.id)
            resto = sendereris - qntdd
            if resto >= 0:
                xp.set_eris(user.id, -qntdd)
                xp.set_eris(member.id, qntdd)
                embed2 = discord.Embed(title='💠 transação', description='{} doou {} Eris para {}.'.format(user.name, qntdd, member.name))
                await self.bot.say(embed=embed2)
            else:
                await self.bot.say('Você não possui saldo suficiente para esta transação')    
        

    @commands.command(pass_context=True)
    async def eris(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        eris = xp.get_eris(member.id)
        embed1 = discord.Embed(title='💠 Eris', description='{} tem {} Eris!'.format(member.name, eris))
        await self.bot.say(embed=embed1)

    @commands.command(pass_context=True)
    async def xp(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        await self.bot.say("O membro {} possui `{}` XP!".format(member.mention, xp.get_xp(member.id)))

    @commands.command(pass_context=True)
    async def givexp(self, ctx, qntdd:int, member: discord.Member = None):
        if ctx.message.author.id == '182635477977923585':
            if member is None: 
                member = ctx.message.author
            xp.user_add_xp(member.id, qntdd)
            await self.bot.say("Adicionado `{1}` XP! para o membro {0}, novo numero de XP é : `{2}`".format(member.mention, qntdd, xp.get_xp(member.id)))
        else:
            await self.bot.say('Sem roubo de xp por hoje <:NicoSmug:416694328858116106>')


    @commands.command(pass_context=True)
    async def perfil(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        """Exibe o seu perfil ou de um membro."""
        eris = xp.get_eris(member.id)
        xpe = xp.get_xp(member.id)
        level = xp.get_level(member.id)
        barra = xp.get_xpbar(member.id)
        #barra = '<:wbare:419367453613621249><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarm:419367453475209217><:wbarr:419367453802627081>'
        exp = xp.get_exp(member.id)        
        tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
        embedperfil = discord.Embed(title="Perfil do membro: " + member.name, color=0x46EEFF)
        embedperfil.set_thumbnail(url=member.avatar_url)
        embedperfil.add_field(name='Informação', value='Level: {0} ({1})\n{2}\nRank: #1 | XP Total : {3}\nReputação: 0'.format(level, exp, barra, xpe))
        embedperfil.add_field(name='Informação global', value='Level: {0} ({1})\n{2}\nRank: #1'.format(level, exp, barra))
        embedperfil.add_field(name='Eris', value='{} 💠'.format(eris))
        #if member.id=='182635477977923585':
            #embedperfil.add_field(name='Casado com', value='💕 sofia')
        embedperfil.add_field(name='Comando favorito', value='help (18)')  
        embedperfil.add_field(name='Conquistas', value='Nenhuma (ainda!)')
        embedperfil.set_footer(text='membro desde '+ tempo +' | tempo de resposta: 150ms')
        await self.bot.say(embed=embedperfil)



    @commands.command(pass_context=True)
    async def removexp(self, ctx, qntdd:int, member: discord.Member = None):
        if ctx.message.author.id == '182635477977923585':
            if member is None: 
                member = ctx.message.author
            xp.user_add_xp(member.id, -qntdd)
            await self.bot.say("Removido `{1}` XP! do membro {0}, novo numero de XP é : `{2}`".format(member.mention, qntdd, xp.get_xp(member.id)))
        else:
            await self.bot.say('Sem roubo de xp por hoje <:NicoSmug:416694328858116106>')


    async def level_to_scoreboard(self):
        await bot.wait_until_ready()
        while not bot.is_closed:
            server = list(bot.servers)[0]
            outstr = ":scroll:   __**Ranking**__   :scroll: \n\n"
            _count = 0
            for member in server.members:
                memb = discord.utils.get(server.members, id=member.id)
                _count += 1
                xpere = xp.get_xp(memb.id)
                lvl = xp.get_level(memb.id)
                if len(lvl) < 2:
                    lvl = "0" + lvl
                outstr += "%s.  -  **[LVL %s]**    %s  -  `%s XP`\n" % (_count, lvl, memb.name, xpere)
                if _count >= 20:
                    break
            try:
                msg = await self.bot.get_message(channel=discord.utils.get(server.channels, name="419266353762009099"), id="419266431495176202")
                await self.bot.edit_message(msg, outstr[:2000])
            except:
                raise
            await asyncio.sleep(60*10)


    async def on_message(self, message):
        if not message.content.startswith('!'):
            usuario_id = message.author.id
            xp.user_add_xp(usuario_id, random.randint(1, 5))
            author_level = xp.get_level(usuario_id)
            author_xp = xp.get_xp(usuario_id)
            if author_level == 0:
                xp.set_level(usuario_id, 1)
                xp.set_eris(usuario_id, 10)
            upxp = (author_level * author_level)*10
            if author_xp >= upxp:
                nlevel=author_level+1
                xp.set_level(usuario_id, nlevel)
                xp.set_eris(usuario_id, 10)


def setup(bot):
    bot.add_cog(xp(bot))