import testing
from eventos import listar_eventos, data_evento
from ralondario import proximos_eventos_ralondario
import datetime as dt
import tg

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

def procesar_mensaje(txt):
    if 'q onda?' in txt:
        return 'q onda?'
    for patron in ['felicitaciones','felicidades','felicito','feliz','congrats','congratulation']:
        if patron in txt.lower():
            return 'Felicitaciones Charly!'

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
    await msg.channel.send('https://www.cubawiki.com.ar/images/a/a0/Plandeestudios.png')

def c_flan_telegram(args, msg):
    tg.mandar_texto(msg.chat.id, 'https://www.cubawiki.com.ar/images/a/a0/Plandeestudios.png', msg.message_id)

def c_flan_debug(args, msg):
    print('https://www.cubawiki.com.ar/images/a/a0/Plandeestudios.png')

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
    tg.mandar_texto(msg.chat.id, recordatorios(args), msg.message_id)

def c_recordatorios_debug(args, msg):
    print(recordatorios(args))

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

async def c_man_discord(args, msg):
    await msg.channel.send(man(args))

def c_man_telegram(args, msg):
    tg.mandar_texto(msg.chat.id, man(args), msg.message_id)

def c_man_debug(args, msg):
    print(man(args))

async def c_ralondario_discord(args, msg):
    await msg.channel.send(ralondario(args))

def c_ralondario_telegram(args, msg):
    tg.mandar_texto(msg.chat.id, ralondario(args), msg.message_id)

def c_ralondario_debug(args, msg):
    print(ralondario(args))

def ralondario(args):
    info = {}
    if len(args) > 0:
        arg = args[0]
        try:
            n = int(arg)
            info["cantidad"] = n
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
    "flan":{
        "f_discord":c_flan_discord,
        "f_telegram":c_flan_telegram,
        "f_debug":c_flan_debug,
        "ayuda":[
            "Ver el plan de estudios",
            "Responde con la imagen del grafo con el plan de estudios. No toma argumentos."
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
