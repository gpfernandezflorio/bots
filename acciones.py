from eventos import inicializar_eventos
from calendario import corresponde, obtener_eventos_siguientes
from ralondario import proximos_eventos_ralondario
from comandos import recibir_comando

canales = {}
lista_de_eventos = []
eventos_siguientes = []

async def realizar(accion):
    canal = canales[accion["canal"]]
    if (canal):
        servidor = canal[0]
        canal = canal[1]
        if (accion["tipo"] == "CH_MSG"):
            if ("value" in accion):
              await canal.send(accion["valor"])
            elif ("funcion" in accion):
              toda_la_data = globals()
              if accion["funcion"] in toda_la_data:
                await canal.send(toda_la_data[accion["funcion"]]())
        elif (accion["tipo"] == "CH_PERM"):
            await canal.set_permissions(servidor.default_role, send_messages=accion["valor"])

async def acciones_programadas():
    global eventos_siguientes
    if len(eventos_siguientes) == 0:
        eventos_siguientes = obtener_eventos_siguientes(lista_de_eventos)
        if len(eventos_siguientes) == 0:
            return
    if corresponde(eventos_siguientes[0]):
        print("NOW:")
        for evento in eventos_siguientes[1:]:
            print(" * " + evento["nombre"])
            await realizar(evento["accion"])
            # TODO: Si era un evento de una única vez, eliminarlo
        eventos_siguientes = []

async def conectar(cliente):
    global lista_de_eventos
    lista_de_eventos = inicializar_eventos()
    if (cliente):
        for guild in cliente.guilds:
            for c in guild.channels:
                canales[c.id] = [guild,c]

def conectar_debug():
    global lista_de_eventos
    lista_de_eventos = inicializar_eventos()
    eventos_siguientes = obtener_eventos_siguientes(lista_de_eventos)
    print(proximos_eventos_ralondario())

async def recibir_mensaje(message):
    if 'q onda?' in message.content:
        await message.channel.send('q onda?')
    else:
        await recibir_comando(message)
