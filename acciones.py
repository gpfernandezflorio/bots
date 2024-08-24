import discord
from eventos import inicializar_eventos, listar_eventos
from calendario import corresponde, obtener_eventos_siguientes
from ralondario import proximos_eventos_ralondario, proxima_tesis
from comandos import recibir_comando, ejecutar_comando_discord, ejecutar_comando_debug, ejecutar_comando_telegram, imagen_proxima_tesis
from triggers import procesar_mensaje
from canales import agregar_canal, obtener_canal, inicializar_canales
import tg
import testing
from fechayhora import justo_ahora

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
                    tg.mandar_texto_revisando_ultimo_mensaje(grupo, valor)
            elif type(valor) == type([]):
                for v in valor:
                    if (a_discord):
                        await canal.send(v)
                    if (a_telegram):
                        tg.mandar_texto_revisando_ultimo_mensaje(grupo, v)
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
    try:
      if len(eventos_siguientes) == 0:
          eventos_siguientes = obtener_eventos_siguientes(listar_eventos())
          if len(eventos_siguientes) == 0:
              return
      if corresponde(eventos_siguientes[0]):
          testing.logTxt("NOW:")
          for evento in eventos_siguientes[1:]:
              testing.logTxt(" * " + evento["nombre"])
              await realizar(evento["accion"])
              # TODO: Si era un evento de una única vez, eliminarlo
          eventos_siguientes = []
    except Exception as e:
      testing.logExcp(e, "Error al procesar las acciones programadas")
      return

def conectar_sin_discord():
    inicializar_eventos()

async def conectar_con_discord(cliente):
    conectar_sin_discord()
    inicializar_canales()
    if (cliente):
        for guild in cliente.guilds:
            for c in guild.channels:
                agregar_canal(guild, c)

def conectar_debug():
    conectar_sin_discord()
    ## DEBUG:
    #eventos_siguientes = obtener_eventos_siguientes(listar_eventos())
    #print(proximos_eventos_ralondario())
    #tg.mandar_archivo('-227382142', 'files/heman.jpg')
    #proxima_tesis()
    #tg.mandar_texto('-1001067544716', 'Ignoren eso')
    debug_chat()

def debug_chat():
    while(True):
        mensaje = input("SEND: ")
        if len(mensaje)==0:
            break
        info_comando = recibir_comando(mensaje)
        if info_comando["OK"]:
            ejecutar_comando_debug(info_comando["comando"], info_comando["argumentos"], mensaje)
        else:
            respuesta = procesar_mensaje(mensaje, "debug")
            if not (respuesta is None):
                print(respuesta)

def recibir_mensaje_telegram(mensaje):
    info_comando = recibir_comando(mensaje["texto"])
    if info_comando["OK"]:
        ejecutar_comando_telegram(info_comando["comando"], info_comando["argumentos"], mensaje)
    else:
        respuesta = procesar_mensaje(mensaje["texto"], str(mensaje["chat_id"]))
        if not (respuesta is None):
            tg.mandar_texto(mensaje["chat_id"], respuesta, mensaje["msg_id"])

async def recibir_mensaje_discord(message):
    if testing.modo_testing and message.guild.id != testing.id_servidor:
        # Sólo mensajes del servidor de test
        return
    info_comando = recibir_comando(message.content)
    if info_comando["OK"]:
        await ejecutar_comando_discord(info_comando["comando"], info_comando["argumentos"], message)
    else:
        respuesta = procesar_mensaje(message.content, str(message.channel))
        if not (respuesta is None):
            await message.channel.send(respuesta)

def anuncio_proxima_tesis():
    res = []
    tesis = proxima_tesis()
    for t in tesis:
        res.append(imagen_proxima_tesis(t))
        # res.append("¡Felicitaciones " + t[0] + "!")
    return res

def eventos_del_dia():
  if (justo_ahora().weekday() == 6):
      return proximos_eventos_ralondario()
  return proximos_eventos_ralondario({'dias':0})
