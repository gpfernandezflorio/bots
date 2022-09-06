import testing
from eventos import listar_eventos, data_evento
from ralondario import proximos_eventos_ralondario
from canales import obtener_canal
import datetime as dt
import tg
import discord

urlPlanos = {'0':{'0':'https://exactas.uba.ar/wp-content/uploads/2022/03/0I-aulas.pdf'}}
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

async def c_decir_discord(args, msg):
    if (len(args) < 2):
        await msg.channel.send("Faltan argumentos")
    else:
        print(args[0])
        channel = obtener_canal(int(args[0]))
        if (channel is None):
            await msg.channel.send("Id de canal inválido")
        else:
            print(channel)
            await channel[1].send(" ".join(args[1:]))

def c_decir_telegram(args, msg):
    if (len(args) < 2):
        tg.mandar_texto(msg["chat_id"], "Faltan argumentos", msg["msg_id"])
    else:
        try:
            tg.mandar_texto(args[0], " ".join(args[1:]))
        except Exception as e:
            tg.mandar_texto(msg["chat_id"], "Id de canal inválido", msg["msg_id"])

def c_decir_debug(args, msg):
    print("id (ignorado): " + args[0])
    print(" ".join(args[1:]))

async def c_sticker_discord(args, msg):
    await msg.channel.send("Aún no implementado")

def c_sticker_telegram(args, msg):
    if (len(args) < 2):
        tg.mandar_texto(msg["chat_id"], "Faltan argumentos", msg["msg_id"])
    else:
        try:
            tg.mandar_sticker(args[0], args[1])
        except Exception as e:
            tg.mandar_texto(msg["chat_id"], "Id de canal o de sticker inválido", msg["msg_id"])

def c_sticker_debug(args, msg):
    print("Mandar " + args[1] + " a " + args[0])

async def c_pic_discord(args, msg):
    await msg.channel.send("Aún no implementado")

def c_pic_telegram(args, msg):
    if (len(args) < 2):
        tg.mandar_texto(msg["chat_id"], "Faltan argumentos", msg["msg_id"])
    else:
        try:
            tg.mandar_imagen_por_id(args[0], args[1], " ".join(args[2:]))
        except Exception as e:
            tg.mandar_texto(msg["chat_id"], "Id de canal o de imagen inválido", msg["msg_id"])

def c_pic_debug(args, msg):
    print("Mandar " + args[1] + " a " + args[0])


async def c_plano_discord(args, msg):
    if len(args) == 0:
        await msg.channel.send("¿Plano de qué?")
        return
    if args[0] in urlPlanos:
        if len(args) == 1:
            await msg.channel.send("¿De qué piso?")
            return
        if args[1] in urlPlanos[args[0]]:
            await msg.channel.send(urlPlanos[args[0]][args[1]])
            return
    await msg.channel.send("No tengo esos planos")

def c_plano_telegram(args, msg):
    if len(args) == 0:
        tg.mandar_texto(msg["chat_id"], "¿Plano de qué?", msg["msg_id"])
        return
    if args[0] in urlPlanos:
        if len(args) == 1:
            tg.mandar_texto(msg["chat_id"], "¿De qué piso?", msg["msg_id"])
            return
        if args[1] in urlPlanos[args[0]]:
            tg.mandar_texto(msg["chat_id"], urlPlanos[args[0]][args[1]], msg["msg_id"])
            return
    tg.mandar_texto(msg["chat_id"], "No tengo esos planos", msg["msg_id"])

def c_plano_debug(args, msg):
    if len(args) == 0:
        print("¿Plano de qué?")
        return
    if args[0] in urlPlanos:
        if len(args) == 1:
            print("¿De qué piso?")
            return
        if args[1] in urlPlanos[args[0]]:
            print(urlPlanos[args[0]][args[1]])
            return
    print("No tengo esos planos")

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

async def c_gracias_discord(args, msg):
    await msg.channel.send("De nada")

def c_gracias_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], "De nada", msg["msg_id"])

def c_gracias_debug(args, msg):
    print("De nada")

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
    "say":{
        "f_discord":c_decir_discord,
        "f_telegram":c_decir_telegram,
        "f_debug":c_decir_debug,
        "ayuda":[
            "Enviar un mensaje personalizado",
            "Envía un mensaje de texto a un grupo o canal. " +
            "Se le debe pasar como argumento un id de grupo o de canal y un mensaje de al menos una palabra. " +
            "Ejemplos: \"say 0042 Buenos días\" para mandar \"Buenos días\" al grupo o canal con id 0042 (debe ser un id válido en el que tenga permisos para mandar mensajes)."
        ]
    },
    "sticker":{
        "f_discord":c_sticker_discord,
        "f_telegram":c_sticker_telegram,
        "f_debug":c_sticker_debug,
        "ayuda":[
            "Enviar un sticker",
            "Envía un sticker a un grupo o canal. " +
            "Se le debe pasar como argumento un id de grupo o de canal y un id de sticker. " +
            "Ejemplos: \"sticker 0042 2400\" para mandar el sticker de id 2400 al grupo o canal con id 0042 (debe ser un id válido en el que tenga permisos para mandar mensajes)."
        ]
    },
    "pic":{
        "f_discord":c_pic_discord,
        "f_telegram":c_pic_telegram,
        "f_debug":c_pic_debug,
        "ayuda":[
            "Enviar una imagen",
            "Envía una imagen a un grupo o canal. " +
            "Se le debe pasar como argumento un id de grupo o de canal y un id de imagen. También se le puede pasar un mensaje como epígrafe. " +
            "Ejemplos: \"pic 0042 2400\" para mandar la imagen de id 2400 al grupo o canal con id 0042 sin epígrafe ; \"pic 0042 2400 Hola, ¿cómo te va?\" para mandar la imagen de id 2400 al grupo o canal con id 0042 con el epígrafe \"Hola, ¿cómo te va?\" (debe ser un id válido en el que tenga permisos para mandar mensajes)."
        ]
    },
    "plano":{
        "f_discord":c_plano_discord,
        "f_telegram":c_plano_telegram,
        "f_debug":c_plano_debug,
        "ayuda":[
            "Ver el plano de un piso de un edificio",
            "Responde con el plano de un piso de uno de los edificios de Exactas.",
            "Se le debe pasar como argumento un número de pabellón (0, 1 o 2) y un número de piso (0, o 1).",
            "Ejemplos: \"plano 0 0\" para los planos de la planta baja del cero más infinito."
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
    },
    "gracias":{
        "f_discord":c_gracias_discord,
        "f_telegram":c_gracias_telegram,
        "f_debug":c_gracias_debug,
        "ayuda":[
            "Agradecer",
            "Responde al agradecimiento."
        ]
    }
}
