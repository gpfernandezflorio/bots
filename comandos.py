import testing
from eventos import listar_eventos, data_evento
from ralondario import proximos_eventos_ralondario
import datetime as dt
import tg
import discord

urlFlan = 'https://www.cubawiki.com.ar/images/a/a0/Plandeestudios.png'
fileFlan = "files/flan.png"

def es_para_mi(msg):
    comando = None
    if msg.startswith("<@!"+str(testing.id_me)+">") or msg.startswith("<@&"+str(testing.id_rol)+">"):
        comando = msg[msg.find('>')+1:]
    elif msg[:4].lower() == "tina":
        comando = msg[4:]
    if not (comando is None):
        while len(comando) > 0 and comando[0] == ' ':
            comando = comando[1:]
        if len(comando) == 0:
            return None
        return comando
    return None

def recibir_comando(msg):
  info_comando = {"OK":False}
  comando = es_para_mi(msg)
  if comando is None:
      return info_comando
  delimitador = comando.find(' ')
  argumentos = []
  if delimitador > 0:
      argumentos = comando[delimitador+1:]
      while len(argumentos) > 0 and argumentos[0] == ' ':
          argumentos = argumentos[1:]
      if len(argumentos) == 0:
        argumentos = []
      else:
        argumentos = argumentos.split(' ');
      comando = comando[:delimitador]
  info_comando["comando"] = comando
  info_comando["argumentos"] = argumentos
  info_comando["OK"] = True
  return info_comando

async def ejecutar_comando_discord(comando, argumentos, msg):
    if (comando in comandos_validos):
        await comandos_validos[comando]['f_discord'](argumentos, msg)

def ejecutar_comando_telegram(comando, argumentos, msg):
    if (comando in comandos_validos):
        comandos_validos[comando]['f_telegram'](argumentos, msg)

def ejecutar_comando_debug(comando, argumentos, msg):
    if (comando in comandos_validos):
        comandos_validos[comando]['f_debug'](argumentos, msg)

async def c_flan_discord(args, msg):
    if len(args) == 0 or (len(args) > 0 and args[0] == 'v'):
        await msg.channel.send(urlFlan)
    elif len(args) > 0 and args[0] == 'n':
        await msg.channel.send(file=discord.File(fileFlan))

def c_flan_telegram(args, msg):
    if len(args) == 0 or (len(args) > 0 and args[0] == 'v'):
        tg.mandar_texto(msg["chat_id"], urlFlan, msg["msg_id"])
    elif len(args) > 0 and args[0] == 'n':
        tg.mandar_archivo(msg["chat_id"], fileFlan)

def c_flan_debug(args, msg):
    if len(args) == 0 or (len(args) > 0 and args[0] == 'v'):
        print(urlFlan)
    elif len(args) > 0 and args[0] == 'n':
        print(fileFlan)

def recordatorios(args):
    txt = "Lista de tareas:"
    if len(args) == 0:
        for evento in listar_eventos():
            txt += "\n " + evento["nombre"]
    else:
        nombre = args[0]
        for evento in listar_eventos():
            if evento["nombre"] == nombre:
                return data_evento(evento)
        txt = "Tarea inexistente: " + nombre
    return txt

async def c_recordatorios_discord(args, msg):
    await msg.channel.send(recordatorios(args))

def c_recordatorios_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], recordatorios(args), msg["msg_id"])

def c_recordatorios_debug(args, msg):
    print(recordatorios(args))

origenes = [
    {
        'claves': ['cubawiki'],
        'rta': "CUBA = Computación UBA\n\nO sea.. es meme, pero tiene sentido."
    }
]

def porque(args):
    if len(args) == 0:
        return "Tenés que pasarme como argumento aquello sobre lo que querés saber el origen."
    clave = args[0].lower()
    for o in origenes:
        if clave in o['claves']:
            return o['rta']
    return "No conozco el origen de eso."

def man(args):
    txt = "Lista de comandos:"
    if len(args) == 0:
        for comando in comandos_validos.keys():
            txt += "\n " + comando + " - " + comandos_validos[comando]["ayuda"][0]
    else:
        nombre = args[0]
        if nombre in comandos_validos:
            return "[[" + nombre + "]]\n" + comandos_validos[nombre]["ayuda"][1]
        txt = "Comando inexistente: " + nombre
    return txt

async def c_porque_discord(args, msg):
    await msg.channel.send(porque(args))

def c_porque_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], porque(args), msg["msg_id"])

def c_porque_debug(args, msg):
    print(porque(args))

async def c_man_discord(args, msg):
    await msg.channel.send(man(args))

def c_man_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], man(args), msg["msg_id"])

def c_man_debug(args, msg):
    print(man(args))

async def c_ralondario_discord(args, msg):
    respuesta = ralondario(args)
    if not (respuesta is None):
        await msg.channel.send(ralondario(args))

def c_ralondario_telegram(args, msg):
    respuesta = ralondario(args)
    if not (respuesta is None):
        tg.mandar_texto(msg["chat_id"], respuesta, msg["msg_id"])

def c_ralondario_debug(args, msg):
    print(ralondario(args))

def ralondario(args):
    info = {}
    if len(args) > 0:
        arg = args[0]
        try:
            n = int(arg)
            info["cantidad"] = n
            if n < 1:
                return None
            info["recortar_en"] = "cantidad"
        except:
            fecha = arg.split("/")
            if len(fecha) == 2:
                try:
                    dia = int(fecha[0])
                    mes = int(fecha[1])
                    hoy = dt.date.today()
                    fecha = dt.date(hoy.year, mes, dia)
                    if fecha < hoy:
                        fecha = fecha.replace(year = fecha.year + 1)
                    info["dias"] = (fecha - hoy).days
                    info["recortar_en"] = "dias"
                except:
                    pass
    return proximos_eventos_ralondario(info)

comandos_validos = {
    "man":{
        "f_discord":c_man_discord,
        "f_telegram":c_man_telegram,
        "f_debug":c_man_debug,
        "ayuda":[
            "Ver lista de comandos",
            "Responde con la lista de comandos y una breve descripción de cada uno. " +
            "Si se le pasa como argumento el nombre de un comando en lugar de listarlos todos devuelve los detalles de dicho comando. " +
            "Ejemplos: \"man\" para la lista de comandos ; \"man man\" para los detalles del comando man."
        ]
    },
    "porque":{
        "f_discord":c_porque_discord,
        "f_telegram":c_porque_telegram,
        "f_debug":c_porque_debug,
        "ayuda":[
            "Preguntar por qué algo está hecho de esa forma",
            "Responde con el origen de alguna de esas cosas que en 10 años van a preguntar wtf por qué esto está hecho así.",
            "Se le debe pasar como argumento aquello de lo cual se quiere conocer su origen."
        ]
    },
    "flan":{
        "f_discord":c_flan_discord,
        "f_telegram":c_flan_telegram,
        "f_debug":c_flan_debug,
        "ayuda":[
            "Ver el plan de estudios",
            "Responde con la imagen del grafo con el plan de estudios.",
            "Se le puede pasar 'n' para el nuevo o 'v' para el viejo."
        ]
    },
    "tasks":{
        "f_discord":c_recordatorios_discord,
        "f_telegram":c_recordatorios_telegram,
        "f_debug":c_recordatorios_debug,
        "ayuda":[
            "Listar tareas periódicas",
            "Responde con la lista de tareas agendadas. " +
            "Si se le pasa como argumento el nombre de una tarea en lugar de listarlas todas devuelve los detalles de dicha tarea. " +
            "Ejemplos: \"tasks\" para la lista de tareas ; \"task ABRIR_LA_NORIEGA\" para los detalles de la tarea que abre la Noriega."
        ]
    },
    "cal":{
        "f_discord":c_ralondario_discord,
        "f_telegram":c_ralondario_telegram,
        "f_debug":c_ralondario_debug,
        "ayuda":[
            "Mostrar calendario académico",
            "Responde con una lista de próximos eventos en el calendario académico. " +
            "Si se le pasa como argumento un número devuelve esa cantidad de eventos. " +
            "Si se le pasa como argumento una fecha (dos números separados por una diagonal) devuelve todos los eventos hasta esa fecha inclusive. " +
            "Si no se le pasa ningún argumento muestra hasta 10 eventos dentro de los próximos 7 días. " +
            "Ejemplos: \"cal\" para ver hasta 10 eventos de la próxima semana ; \"cal 5\" para ver los próximos 5 eventos ; \"cal 10/5\" para ver los eventos hasta el 10 de mayo."
        ]
    }
}
