from eventos import eventos
from calendario import corresponde

canales = {}

async def realizar(accion):
    canal = canales[accion["canal"]]
    if (canal):
        servidor = canal[0]
        canal = canal[1]
        if (accion["tipo"] == "CH_MSG"):
            await canal.send(accion["valor"])
        elif (accion["tipo"] == "CH_PERM"):
            await canal.set_permissions(servidor.default_role, send_messages=accion["valor"])

async def acciones_programadas():
    for evento in eventos:
        if corresponde(evento["cuando"]):
            await realizar(evento["accion"])

async def conectar(cliente):
    for guild in cliente.guilds:
        for c in guild.channels:
            canales[c.id] = [guild,c]

async def recibir_mensaje(message):
    if message.content == 'q onda?':
        await message.channel.send(message.content)
