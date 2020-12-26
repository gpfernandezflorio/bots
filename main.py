import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
from acciones import conectar, conectar_debug, acciones_programadas, recibir_mensaje
from datetime import datetime

def main():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DEBUG = os.getenv('DEBUG')=="YES"

    @tasks.loop(minutes=1)
    async def una_vez_por_minuto():
        await acciones_programadas()

    if (DEBUG):
        conectar_debug()
    else:
        client = discord.Client()

        @client.event
        async def on_message(message): # Cuando alguien dice "q onda?", respondo lo mismo
            if message.author == client.user:
                return
            await recibir_mensaje(message)

        @client.event
        async def on_ready():
            await conectar(client)
            una_vez_por_minuto.start()
            print(str(datetime.now()) + " READY")

        client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
