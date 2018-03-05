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

async def get_server_codigo(server_id):
    try:
        conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
        codigo = await conn.fetch('''SELECT codigo FROM public.servercodigo WHERE serverid ={} and ligado =1'''.format(server_id))       
        codigor = codigo[0]
        codigo = codigor['codigo']
        await conn.close()
        return codigo
    except:
        return 0

async def get_server_codigo_ligado(server_id):
    try:
        conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
        ligado = await conn.fetch('''SELECT ligado FROM public.servercodigo WHERE serverid ={}'''.format(server_id))       
        ligador = ligado[0]
        ligado = ligador['ligado']
        await conn.close()
        return ligado
    except:        
        return 0

async def set_server_codigo(server_id, codigo):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    await conn.fetch('''UPDATE public.servercodigo SET codigo = '{}' WHERE serverid ={}'''.format(codigo, server_id))       
    await conn.close()

async def set_server_codigo_ligado(server_id, nligado):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    ligado = await conn.fetch('''SELECT ligado FROM public.servercodigo WHERE serverid ={}'''.format(server_id))       
    ligador = ligado[0]
    ligado = ligador['ligado']
    if ligado == nligado:    
        await conn.close()
        return 0
    else:
        await conn.fetch('''UPDATE public.servercodigo SET ligado = {0} WHERE serverid ={1}'''.format(nligado, server_id))       
        await conn.close()
        return 0

async def get_canal_codigo(server_id):
    try:
        conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
        canal_codigo = await conn.fetch('''SELECT canal_codigo FROM public.servercodigo WHERE serverid ={}'''.format(server_id))       
        canal_codigor = canal_codigo[0]
        canal_codigo = canal_codigor['canal_codigo']
        await conn.close()
        return canal_codigo
    except:        
        return 0

async def set_canal_codigo(server_id, canal_codigo):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    canal_codigo = await conn.fetch('''SELECT canal_codigo FROM public.serverusers WHERE serverid ={}'''.format(server_id))       
    canal_codigor = canal_codigo[0]
    canal_codigo = canal_codigor['canal_codigo']
    await conn.fetch('''UPDATE public.servercodigo SET canal_codigo = {0} WHERE serverid ={1}'''.format(canal_codigo, server_id))       
    await conn.close()

async def get_canal_regras(server_id):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    canal_regras = await conn.fetch('''SELECT canal_regras FROM public.servercodigo WHERE serverid ={}'''.format(server_id))       
    canal_regrasr = canal_regras[0]
    canal_regras = canal_regrasr['canal_regras']
    await conn.close()
    return canal_regras


async def set_canal_regras(server_id, canal_regras):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    canal_regras = await conn.fetch('''SELECT canal_regras FROM public.serverusers WHERE serverid ={}'''.format(server_id))       
    canal_regrasr = canal_regras[0]
    canal_regras = canal_regrasr['canal_regras']
    await conn.fetch('''UPDATE public.servercodigo SET canal_regras = {0} WHERE serverid ={1}'''.format(canal_regras, server_id))       
    await conn.close()

async def get_cargo_membro(server_id):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    cargo_membro = await conn.fetch('''SELECT cargo_membro FROM public.servercodigo WHERE serverid ={}'''.format(server_id))       
    cargo_membror = cargo_membro[0]
    cargo_membro = cargo_membror['cargo_membro']
    await conn.close()
    return cargo_membro


async def set_cargo_membro(server_id, cargo_membro):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    cargo_membro = await conn.fetch('''SELECT cargo_membro FROM public.serverusers WHERE serverid ={}'''.format(server_id))       
    cargo_membror = cargo_membro[0]
    cargo_membro = cargo_membror['cargo_membro']
    await conn.fetch('''UPDATE public.servercodigo SET cargo_membro = {0} WHERE serverid ={1}'''.format(cargo_membro, server_id))       
    await conn.close()

async def get_msgcode(server_id):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    msgcode = await conn.fetch('''SELECT msg_codigo FROM public.servercodigo WHERE serverid ={}'''.format(server_id))       
    msgcoder = msgcode[0]
    msgcode = msgcoder['msg_codigo']
    await conn.close()
    return msgcode


async def set_msgcode(server_id, msgcode):
    conn = await asyncpg.connect(user=dbuser, password=dbpassword, database=dbdatabase, host=dbhost)        
    msgcode = await conn.fetch('''SELECT msgcode FROM public.serverusers WHERE serverid ={}'''.format(server_id))       
    msgcoder = msgcode[0]
    msgcode = msgcoder['msg_codigo']
    await conn.fetch('''UPDATE public.servercodigo SET msg_codigo = {0} WHERE serverid ={1}'''.format(msgcode, server_id))       
    await conn.close()
