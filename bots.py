# bots.py
import os
import asyncio
from datetime import datetime
import discord
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
servidor = "DC"
#servidor = "TEST"
TOKEN = os.getenv('DISCORD_TOKEN')
id_servidor = os.getenv('DISCORD_GUILD_'+servidor)
id_canal_noriega = os.getenv('DISCORD_CH_'+servidor+'_NORIEGA')
id_canal_general = os.getenv('DISCORD_CH_'+servidor+'_GENERAL')

servidor_conectado = None
canal_noriega = None
canal_general = None
hora_mensaje_cierre = [17,55] # A esta hora mando "en 5 cierra la noriega"
mensaje_cierre = "Atención: En 5 mimitos se cierra la Noriega"
client = discord.Client()

def cuanto_falta(objetivo):
    now = datetime.now()
    hora = now.hour
    minutos = now.minute
    if (minutos > objetivo[1]):
        objetivo[1] += 60
        objetivo[0] -= 1
    if (hora > objetivo[0]):
        objetivo[0]+=24
    elif (hora == objetivo[0]):
        if (minutos > objetivo[1]):
            objetivo[0]+=24
    return [objetivo[0]-hora,objetivo[1]-minutos]

@client.event
async def on_ready(): # Al iniciar, se conecta al servidor
    await conectar_al_servidor()

@client.event
async def on_message(message): # Cuando alguien dice "q onda?", respondo lo mismo
    if message.author == client.user:
        return
    await recibir_mensaje(message)

@tasks.loop(hours=24)
async def en_5_cierra_la_noriega(): # Una vez por día mando el aviso de que se cierra la noriega
    if canal_noriega:
        await canal_noriega.send(mensaje_cierre)
        if servidor_conectado:
            await asyncio.sleep(4*60)
            try:
                await canal_noriega.set_permissions(servidor_conectado.default_role, send_messages=False)
            except Exception as e:
                pass

@en_5_cierra_la_noriega.before_loop
async def before():
    delta = cuanto_falta(hora_mensaje_cierre)
    print(f"Próximo en {delta[0]}:{delta[1]}")
    segundos_restantes = delta[0]*3600 + delta[1]*60
    await asyncio.sleep(segundos_restantes)

async def conectar_al_servidor():
    global servidor_conectado, canal_noriega, canal_general
    for guild in client.guilds:
        #print(f'{guild.name}(id: {guild.id})')
        #for c in guild.channels:
        #    print(f'{c.name}(id: {c.id})')
        if str(guild.id) == id_servidor:
            servidor_conectado = guild
            break
    if (servidor_conectado):
        print(f'servidor encontrado: {servidor_conectado.name}')
        for c in servidor_conectado.channels:
            if str(c.id) == id_canal_noriega:
                canal_noriega = c
            if str(c.id) == id_canal_general:
                canal_general = c
        if (canal_noriega):
            print(f'canal encontrado: {canal_noriega.name}')
            en_5_cierra_la_noriega.start()
        else:
            print("Error: no encontré el canal de la Noriega")
            exit(0)
        if (canal_general):
            print(f'canal encontrado: {canal_general.name}')
        else:
            print("Error: no encontré el canal general")
            exit(0)
    else:
        print("Error: no me pude conectar al servidor")
        exit(0)

async def recibir_mensaje(message): # Ojo: funciona con cualquier canal de cualquier servidor
    if message.content == 'q onda?':
        await message.channel.send(message.content)

client.run(TOKEN)
