import testing
from eventos import listar_eventos, data_evento

def es_para_mi(msg):
    if type(msg) == type(""):
        return msg
    comando = None
    if msg.content.startswith("<@!"+str(testing.id_me)+">") or msg.content.startswith("<@&"+str(testing.id_rol)+">"):
        comando = msg.content[msg.content.find('>')+1:]
    elif msg.content[:4].lower() == "tina":
        comando = msg.content[4:]
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

async def ejecutar_comando(comando, argumentos, msg):
    if (comando in comandos_validos):
        await comandos_validos[comando]['f'](argumentos, msg)

def ejecutar_comando_debug(comando, argumentos, msg):
    if (comando in comandos_validos):
        comandos_validos[comando]['f_debug'](argumentos, msg)

async def c_flan(args, msg):
    await msg.channel.send('https://www.cubawiki.com.ar/images/a/a0/Plandeestudios.png')

def c_flan_debug(args, msg):
    print('https://www.cubawiki.com.ar/images/a/a0/Plandeestudios.png')

def recordatorios(args, msg):
    txt = "Lista de recordatorios:"
    if len(args) == 0:
        for evento in listar_eventos():
            txt += "\n " + evento["nombre"]
    else:
        nombre = args[0]
        for evento in listar_eventos():
            if evento["nombre"] == nombre:
                return data_evento(evento)
        txt = "Recordatorio inexistente: " + nombre
    return txt

async def c_recordatorios(args, msg):
    await msg.channel.send(recordatorios(args, msg))

def c_recordatorios_debug(args, msg):
    print(recordatorios(args, msg))

comandos_validos = {
    "flan":{
        "f":c_flan,
        "f_debug":c_flan_debug
    },
    "recordatorios":{
        "f":c_recordatorios,
        "f_debug":c_recordatorios_debug
    }
}
