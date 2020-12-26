from eventos import inicializar_eventos
from calendario import corresponde
from comandos import recibir_comando

canales = {}
lista_de_eventos = []

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
    for evento in lista_de_eventos:
        if corresponde(evento["cuando"]):
            await realizar(evento["accion"])

async def conectar(cliente):
    global lista_de_eventos
    for guild in cliente.guilds:
        for c in guild.channels:
            canales[c.id] = [guild,c]
    lista_de_eventos = await inicializar_eventos()

async def recibir_mensaje(message):
    if 'q onda?' in message.content:
        await message.channel.send('q onda?')
    else:
        await recibir_comando(message)
