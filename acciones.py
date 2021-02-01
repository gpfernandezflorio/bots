from eventos import inicializar_eventos
from calendario import corresponde, obtener_proximo_evento
from ralondario import proximos_eventos_ralondario
from comandos import recibir_comando

canales = {}
lista_de_eventos = []
proximo_evento = None

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
    global proximo_evento
    if (proximo_evento is None):
        proximo_evento = obtener_proximo_evento(lista_de_eventos)
        if (proximo_evento is None):
            return
    if corresponde(proximo_evento[0]):
        print("NOW!")
        await realizar(proximo_evento[1]["accion"])
        proximo_evento = None
        # TODO: Si era un evento de una única vez, eliminarlo

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
    proximo_evento = obtener_proximo_evento(lista_de_eventos)
    print(proximos_eventos_ralondario())

async def recibir_mensaje(message):
    if 'q onda?' in message.content:
        await message.channel.send('q onda?')
    else:
        await recibir_comando(message)
