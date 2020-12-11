import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
from acciones import conectar, acciones_programadas
from datetime import datetime

def main():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

    @tasks.loop(minutes=1)
    async def una_vez_por_minuto():
        await acciones_programadas()

    client = discord.Client()

    @client.event
    async def on_ready():
        await conectar(client)
        print(str(datetime.now()) + " READY")
        una_vez_por_minuto.start()

    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
