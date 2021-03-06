import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
from acciones import conectar, conectar_debug, acciones_programadas, recibir_mensaje_discord, recibir_mensaje_telegram
from datetime import datetime
import tg

INICIADO = False

def main():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DEBUG = os.getenv('DEBUG')=="YES"

    @tasks.loop(minutes=1)
    async def una_vez_por_minuto():
        # Recibir mensajes de TG:
        for mensaje in tg.recibir_mensajes():
            recibir_mensaje_telegram(mensaje)
        await acciones_programadas()

    if (DEBUG):
        conectar_debug()
    else:
        client = discord.Client()
        tg.inicializar()

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            await recibir_mensaje_discord(message)

        @client.event
        async def on_ready():
            global INICIADO
            await conectar(client)
            if not INICIADO:
                una_vez_por_minuto.start()
                INICIADO = True
            print(str(datetime.now()) + " READY")

        client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
