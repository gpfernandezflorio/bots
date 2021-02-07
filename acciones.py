from eventos import inicializar_eventos, listar_eventos
from calendario import corresponde, obtener_eventos_siguientes
from ralondario import proximos_eventos_ralondario
from comandos import recibir_comando, ejecutar_comando, ejecutar_comando_debug
from canales import agregar_canal, obtener_canal

eventos_siguientes = []

async def realizar(accion):
    canal = obtener_canal(accion["canal"])
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
        eventos_siguientes = obtener_eventos_siguientes(listar_eventos())
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
    inicializar_eventos()
    if (cliente):
        for guild in cliente.guilds:
            for c in guild.channels:
                agregar_canal(guild, c)

def conectar_debug():
    inicializar_eventos()
    eventos_siguientes = obtener_eventos_siguientes(listar_eventos())
    print(proximos_eventos_ralondario())
    debug_chat()

def debug_chat():
    while(True):
        msg = input("SEND: ")
        if len(msg)==0:
            break
        info_comando = recibir_comando(msg)
        if info_comando["OK"]:
            ejecutar_comando_debug(info_comando["comando"], info_comando["argumentos"], msg)

async def recibir_mensaje(message):
    if 'q onda?' in message.content:
        await message.channel.send('q onda?')
        return
    for patron in ['felicitaciones','felicidades','felicito','feliz','congrats','congratulation']:
        if patron in message.content.lower():
            await message.channel.send('Felicitaciones Charly!')
            return
    info_comando = recibir_comando(message)
    if info_comando["OK"]:
        await ejecutar_comando(info_comando["comando"], info_comando["argumentos"], message)
