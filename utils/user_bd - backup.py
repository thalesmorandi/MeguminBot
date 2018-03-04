import discord
import random
import os
import json
import os.path
import asyncpg
    
async def get_xp(user_id):
    try:
        conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
        xp = await conn.fetch('''SELECT xp FROM public.users WHERE ID ={}'''.format(user_id))       
        xpr = xp[0]
        xp = xpr['xp']
        await conn.close()
        return xp
    except:
        return 0

async def get_level(user_id):
    try:
        conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
        level = await conn.fetch('''SELECT level FROM public.users WHERE ID ={}'''.format(user_id))       
        levelr = level[0]
        level = levelr['level']
        await conn.close()
        return level

    except:        
        return 1

async def get_eris(user_id):
    try:
        conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
        eris = await conn.fetch('''SELECT eris FROM public.users WHERE ID ={}'''.format(user_id))       
        erisr = eris[0]
        eris = erisr['eris']
        await conn.close()
        return eris
    except:        
        return 10

async def get_rep(user_id):
    try:
        conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
        rep = await conn.fetch('''SELECT rep FROM public.users WHERE ID ={}'''.format(user_id))       
        repr = rep[0]
        rep = repr['rep']
        await conn.close()
        return rep
    except:        
        return 0

async def set_rep(user_id: int, repadd: int):
    conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
    rep = await conn.fetch('''SELECT rep FROM public.users WHERE ID ={}'''.format(user_id))       
    repr = rep[0]
    rep = repr['rep']
    await conn.fetch('''UPDATE public.users SET rep = {0} WHERE ID = {1}'''.format(rep+repadd, user_id))       
    await conn.close()

async def set_xp(user_id, xpadd: int):
    conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
    xp = await conn.fetch('''SELECT xp FROM public.users WHERE ID ={}'''.format(user_id))       
    try:
        xpr = xp[0]
        xp = xpr['xp']
        await conn.fetch('''UPDATE public.users SET xp = {0} WHERE ID = {1}'''.format(xp+xpadd, user_id))       
        await conn.close()
    except:
        await conn.fetch('''INSERT INTO public.users (id, xp, level, eris, rep) VALUES ({0}, {1}, 1, 10, 0)'''.format(user_id, xpadd))       
        await conn.close()

async def set_level(user_id, leveladd: int):
    conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
    level = await conn.fetch('''SELECT level FROM public.users WHERE ID ={}'''.format(user_id))       
    levelr = level[0]
    level = levelr['level']
    await conn.fetch('''UPDATE public.users SET level = {0} WHERE ID = {1}'''.format(level+leveladd, user_id))       
    await conn.close()


async def set_eris(user_id: int, erisadd: int):
    conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
    eris = await conn.fetch('''SELECT eris FROM public.users WHERE ID ={}'''.format(user_id))       
    erisr = eris[0]
    eris = erisr['eris']
    await conn.fetch('''UPDATE public.users SET eris = {0} WHERE ID = {1}'''.format(eris+erisadd, user_id))       
    await conn.close()

async def get_exp(user_id:int):
    xp = await get_xp(user_id)
    level = await get_level(user_id)
    if level > 1:
        levelcalc = level-1
        xpcalc = ((levelcalc*levelcalc)*10)
        xpatual =xp - xpcalc
        xpcalc = ((level*level)*10)-xpcalc
        exp= str(str(xpatual)+'/'+str(xpcalc))
        return exp
    else:
        exp= str(xp)+'/10'
        return exp          

async def get_xpbar(user_id:int):
    xp = await get_xp(user_id)
    level = await get_level(user_id)
    if level > 1:
        levelcalc = level-1#1
        xpcalc = ((levelcalc*levelcalc)*10)#10
        xpatual = xp - xpcalc #25
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
        xpatual =xp - xpcalc #25
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

###########################################LOCAL GETTER#########################

async def get_local_xp(server_id, user_id):
    try:
        conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
        xp = await conn.fetch('''SELECT localxp FROM public.serverusers WHERE serverid ={} and memberid ={}'''.format(server_id, user_id))       
        xpr = xp[0]
        xp = xpr['localxp']
        await conn.close()
        return xp
    except:
        return 0

async def get_local_level(server_id, user_id):
    try:
        conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
        level = await conn.fetch('''SELECT locallevel FROM public.serverusers WHERE serverid ={} and memberid ={}'''.format(server_id, user_id))       
        levelr = level[0]
        level = levelr['locallevel']
        await conn.close()
        return level

    except:        
        return 1

async def set_local_xp(server_id, user_id, xpadd: int):
    conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
    xp = await conn.fetch('''SELECT localxp FROM public.serverusers WHERE serverid ={} and memberid ={}'''.format(server_id, user_id))       
    try:
        xpr = xp[0]
        xp = xpr['localxp']
        await conn.fetch('''UPDATE public.serverusers SET localxp = {0} WHERE serverid ={1} and memberid ={2}'''.format(xp+xpadd, server_id, user_id))       
        await conn.close()
    except:
        await conn.fetch('''INSERT INTO public.serverusers (serverid, memberid, localxp, locallevel) VALUES ({0}, {1}, {2}, 1)'''.format(server_id, user_id, xpadd))       
        await conn.close()

async def set_local_level(server_id, user_id, leveladd: int):
    conn = await asyncpg.connect(user='postgres', password='8381850', database='teste', host='127.0.0.1')        
    level = await conn.fetch('''SELECT locallevel FROM public.serverusers WHERE serverid ={} and memberid ={}'''.format(server_id, user_id))       
    levelr = level[0]
    level = levelr['locallevel']
    await conn.fetch('''UPDATE public.serverusers SET locallevel = {0} WHERE serverid ={1} and memberid ={2}'''.format(level+leveladd,server_id, user_id))       
    await conn.close()

async def get_local_exp(server_id, user_id:int):
    xp = await get_local_xp(server_id, user_id)
    level = await get_local_level(server_id, user_id)
    if level > 1:
        levelcalc = level-1
        xpcalc = ((levelcalc*levelcalc)*10)
        xpatual =xp - xpcalc
        xpcalc = ((level*level)*10)-xpcalc
        exp= str(str(xpatual)+'/'+str(xpcalc))
        return exp
    else:
        exp= str(xp)+'/10'
        return exp  

async def get_local_xpbar(server_id, user_id:int):
    xp = await get_local_xp(server_id, user_id)
    level = await get_local_level(server_id, user_id)
    if level > 1:
        levelcalc = level-1#1
        xpcalc = ((levelcalc*levelcalc)*10)#10
        xpatual = xp - xpcalc #25
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
        xpatual =xp - xpcalc #25
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