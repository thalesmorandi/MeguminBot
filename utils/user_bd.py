import discord
import random
import os
import json
import os.path
import asyncpg
is_prod = os.environ.get('IS_HEROKU', None)


if is_prod:
    dbuser = os.environ.get('USER')
    dbpassword = os.environ.get('PASSWORD')
    dbdatabase = os.environ.get('DATABASE')
    dbhost = os.environ.get('HOST')
else:
    from utils import configdb
    dbuser = configdb.dbuser
    dbpassword = configdb.dbpassword
    dbdatabase = configdb.dbdatabase
    dbhost = configdb.dbhost
    
async def get_xp(user_id):
    try:
        conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
        xp = await conn.fetch('''SELECT xp FROM public.users WHERE ID ={}'''.format(user_id))       
        xpr = xp[0]
        xp = xpr['xp']
        await conn.close()
        return xp
    except:
        await conn.close()
        return 0

async def get_level(xp):
        remaining_xp = int(xp)
        level = 0
        while remaining_xp >= 5*(level**2)+50*level+100:
            remaining_xp -= 5*(level**2)+50*level+100
            level += 1
        return level

async def get_eris(user_id):
    try:
        conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
        eris = await conn.fetch('''SELECT eris FROM public.users WHERE ID ={}'''.format(user_id))       
        erisr = eris[0]
        eris = erisr['eris']
        await conn.close()
        return eris
    except:
        await conn.close()        
        return 100

async def get_couple(user_id):
    try:
        conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
        couple = await conn.fetch('''SELECT couple FROM public.users WHERE ID ={}'''.format(user_id))       
        coupler = couple[0]
        couple = coupler['couple']
        await conn.close()
        return couple
    except:
        await conn.close()        
        return None

async def get_rep(user_id):
    try:
        conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
        rep = await conn.fetch('''SELECT rep FROM public.users WHERE ID ={}'''.format(user_id))       
        repr = rep[0]
        rep = repr['rep']
        await conn.close()
        return rep
    except:
        await conn.close()     
        return 0

async def set_rep(user_id: int, repadd: int):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    rep = await conn.fetch('''SELECT rep FROM public.users WHERE ID ={}'''.format(user_id))       
    repr = rep[0]
    rep = repr['rep']
    await conn.fetch('''UPDATE public.users SET rep = {0} WHERE ID = {1}'''.format(rep+repadd, user_id))       
    await conn.close()

async def set_xp(user_id, xpadd: int):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    xp = await conn.fetch('''SELECT xp FROM public.users WHERE ID ={}'''.format(user_id))       
    try:
        xpr = xp[0]
        xp = xpr['xp']
        await conn.fetch('''UPDATE public.users SET xp = {0} WHERE ID = {1}'''.format(xp+xpadd, user_id))       
        await conn.close()
    except:
        await conn.fetch('''INSERT INTO public.users (id, xp, eris, rep) VALUES ({0}, {1}, 100, 0)'''.format(user_id, xpadd))       
        await conn.close()

async def set_eris(user_id: int, erisadd: int):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    eris = await conn.fetch('''SELECT eris FROM public.users WHERE ID ={}'''.format(user_id))       
    erisr = eris[0]
    eris = erisr['eris']
    await conn.fetch('''UPDATE public.users SET eris = {0} WHERE ID = {1}'''.format(eris+erisadd, user_id))       
    await conn.close()

async def set_couple(user_id: int, couple):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    await conn.fetch('''UPDATE public.users SET couple = {0} WHERE ID = {1}'''.format(couple, user_id))       
    await conn.fetch('''UPDATE public.users SET couple = {0} WHERE ID = {1}'''.format(user_id, couple))       
    await conn.close()

async def unset_couple(user_id: int, couple):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)
    await conn.fetch('''UPDATE public.users SET couple = NULL WHERE ID = {}'''.format(couple))       
    await conn.fetch('''UPDATE public.users SET couple = NULL WHERE ID = {}'''.format(user_id))       
    await conn.close()

async def get_exp(user_id:int):
    xp = await get_xp(user_id)
    level = await get_level(xp)
    if level >= 1:
        remaining_xp = xp
        level = 0
        while remaining_xp >= 5*(level**2)+50*level+100:
            remaining_xp -= 5*(level**2)+50*level+100
            level += 1        
        xpcalc = 5*(level**2)+50*level+100
        exp= str(str(remaining_xp)+'/'+str(xpcalc))
        return exp
    else:
        exp= str(xp)+'/100'
        return exp          

async def get_xpbar(user_id:int):
    xp = await get_xp(user_id)
    level = await get_level(xp)
    if level >= 1:
        remaining_xp = xp
        level = 0
        while remaining_xp >= 5*(level**2)+50*level+100:
            remaining_xp -= 5*(level**2)+50*level+100
            level += 1
        xpnlevel = 5*((level+1)**2)+50*level+101       
        barrasverdes = int((remaining_xp/(xpnlevel/6)))
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
        xpatual = xp
        barrasverdes = int(xpatual/(100/6))
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

###########################################LOCAL GETTER#########################

async def get_local_xp(server_id, user_id):
    try:
        conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
        xp = await conn.fetch('''SELECT localxp FROM public.serverusers WHERE serverid ={} and memberid ={}'''.format(server_id, user_id))       
        xpr = xp[0]
        xp = xpr['localxp']
        await conn.close()
        return xp
    except:
        await conn.close()
        return 0

async def get_local_level(xp):
        remaining_xp = int(xp)
        level = 0
        while remaining_xp >= 5*(level**2)+50*level+100:
            remaining_xp -= 5*(level**2)+50*level+100
            level += 1
        return level

async def set_local_xp(server_id, user_id, xpadd: int):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    xp = await conn.fetch('''SELECT localxp FROM public.serverusers WHERE serverid ={} and memberid ={}'''.format(server_id, user_id))       
    try:
        xpr = xp[0]
        xp = xpr['localxp']
        await conn.fetch('''UPDATE public.serverusers SET localxp = {0} WHERE serverid ={1} and memberid ={2}'''.format(xp+xpadd, server_id, user_id))       
        await conn.close()
    except:
        await conn.fetch('''INSERT INTO public.serverusers (serverid, memberid, localxp) VALUES ({0}, {1}, {2})'''.format(server_id, user_id, xpadd))       
        await conn.close()

async def get_local_ranking(server_id):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    ranking = await conn.fetch('''SELECT memberid, localxp FROM public.serverusers WHERE serverid = {} ORDER BY localxp DESC'''.format(server_id))       
    await conn.close()
    return ranking

async def get_ranking():
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    ranking = await conn.fetch('''SELECT id, xp FROM public.users ORDER BY xp DESC''')       
    await conn.close()
    return ranking


async def get_local_exp(server_id, user_id:int):
    xp = await get_local_xp(server_id, user_id)
    level = await get_local_level(xp)
    if level >= 1:
        remaining_xp = xp
        level = 0
        while remaining_xp >= 5*(level**2)+50*level+100:
            remaining_xp -= 5*(level**2)+50*level+100
            level += 1        
        xpcalc = 5*(level**2)+50*level+100
        exp= str(str(remaining_xp)+'/'+str(xpcalc))
        return exp
    else:
        exp= str(xp)+'/100'
        return exp  

async def get_local_xpbar(server_id, user_id:int):
    xp = await get_local_xp(server_id, user_id)
    level = await get_local_level(xp)
    if level >= 1:
        remaining_xp = xp
        level = 0
        while remaining_xp >= 5*(level**2)+50*level+100:
            remaining_xp -= 5*(level**2)+50*level+100
            level += 1
        xpnlevel = 5*((level+1)**2)+50*level+101
        barrasverdes = int((remaining_xp/(xpnlevel/6)))
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
        xpatual = xp
        barrasverdes = int(xpatual/(100/6))
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