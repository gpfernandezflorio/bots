import discord
from eventos import inicializar_eventos, listar_eventos
from calendario import corresponde, obtener_eventos_siguientes
from ralondario import proximos_eventos_ralondario, proxima_tesis
from comandos import recibir_comando, ejecutar_comando_discord, ejecutar_comando_debug, procesar_mensaje
from canales import agregar_canal, obtener_canal, inicializar_canales
import tg
import imageDraw

eventos_siguientes = []

async def realizar(accion):
    a_discord = False
    a_telegram = False
    servidor = None
    canal = obtener_canal(accion.get("canal", None))
    if not (canal is None):
        servidor = canal[0]
        canal = canal[1]
        a_discord = True
    grupo = accion.get("grupo", None)
    if not (grupo is None):
        a_telegram = True
    valor = None
    if ("valor" in accion):
        valor = accion["valor"]
    elif ("funcion" in accion):
      toda_la_data = globals()
      if accion["funcion"] in toda_la_data:
          valor = toda_la_data[accion["funcion"]]()
    if (accion["tipo"] == "CH_MSG"):
        if not (valor is None):
            if type(valor) == type(""):
                if (a_discord):
                    await canal.send(valor)
                if (a_telegram):
                    tg.mandar_texto(grupo, valor)
            elif type(valor) == type([]):
                for v in valor:
                    if (a_discord):
                        await canal.send(v)
                    if (a_telegram):
                        tg.mandar_texto(grupo, v)
    elif (accion["tipo"] == "CH_FILE"):
        if not (valor is None):
            if type(valor) == type(""):
                if (a_discord):
                    await canal.send(file=discord.File(valor))
                if (a_telegram):
                    tg.mandar_archivo(grupo, valor)
            elif type(valor) == type([]):
                for v in valor:
                    if (a_discord):
                        await canal.send(file=discord.File(v))
                    if (a_telegram):
                        tg.mandar_archivo(grupo, v)
    elif (accion["tipo"] == "CH_PERM"):
        if (a_discord):
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
    inicializar_canales()
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

def recibir_mensaje_telegram(texto, chat_id, msg_id):
  print("Recibido: " + texto)
  respuesta = procesar_mensaje(texto)
  if respuesta is None:
      info_comando = recibir_comando(texto)
      if info_comando["OK"]:
          ejecutar_comando_telegram(info_comando["comando"], info_comando["argumentos"], mensaje)
  else:
      tg.mandar_texto(chat_id, respuesta, msg_id)

async def recibir_mensaje_discord(message):
    respuesta = procesar_mensaje(message.content)
    if respuesta is None:
        info_comando = recibir_comando(message.content)
        if info_comando["OK"]:
            await ejecutar_comando_discord(info_comando["comando"], info_comando["argumentos"], message)
    else:
        await message.channel.send(respuesta)

def anuncio_proxima_tesis():
    res = []
    tesis = proxima_tesis()
    for t in tesis:
        res.append(imagen_proxima_tesis(t))
    return res

def imagen_proxima_tesis(tesis):
    tesista = tesis[0]
    hora_tesis = tesis[1]
    outfile = "files/"+tesista.replace(" ","_")+".png"
    imagen = imageDraw.abrir_imagen("files/heman.jpg")
    imagen.escribir(tesista, [120,120], tamanio=30, color=[255,255,255])
    imagen.escribir(hora_tesis, [450,170], tamanio=40, color=[255,255,255])
    imagen.guardar_imagen(outfile)
    return outfile
