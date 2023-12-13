import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
from acciones import conectar_con_discord, conectar_sin_discord, conectar_debug, acciones_programadas, recibir_mensaje_discord, recibir_mensaje_telegram
from fechayhora import justo_ahora
import asyncio
import tg

INICIADO = False

async def una_vez_por_minuto():
    # Recibir mensajes de TG:
    for mensaje in tg.recibir_mensajes():
        recibir_mensaje_telegram(mensaje)
    await acciones_programadas()

def main_sin_discord():
    conectar_sin_discord()
    global INICIADO
    if not INICIADO:
        asyncio.run(una_vez_por_minuto())
        INICIADO = True
    print(str(justo_ahora()) + " READY")
    import time
    while True:
        time.sleep(1000)

def main_con_discord():
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tg.inicializar()

    @tasks.loop(minutes=1)
    async def una_vez_por_minuto_discord():
        await una_vez_por_minuto()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await recibir_mensaje_discord(message)

    @client.event
    async def on_ready():
        global INICIADO
        await conectar_con_discord(client)
        if not INICIADO:
            una_vez_por_minuto_discord.start()
            INICIADO = True
        print(str(justo_ahora()) + " READY")

    client.run(DISCORD_TOKEN)

def main():
    load_dotenv()
    DEBUG = os.getenv('DEBUG')=="YES"
    if (not os.path.isdir('tmp')):
        os.makedirs('tmp')


    if (DEBUG):
        conectar_debug()
    elif (os.getenv('DISCORD_ON')=="YES"):
        main_con_discord()
    else:
        main_sin_discord()


if __name__ == "__main__":
    main()
