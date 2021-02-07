import testing

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
  comando = es_para_mi(msg)
  if comando is None:
      return
  delimitador = comando.find(' ')
  argumentos = None
  if delimitador > 0:
      argumentos = comando[delimitador+1:]
      while len(argumentos) > 0 and argumentos[0] == ' ':
          argumentos = argumentos[1:]
      if len(argumentos) == 0:
        argumentos = None
      comando = comando[:delimitador]
  return comando.lower(), argumentos

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

comandos_validos = {
    "flan":{
        "f":c_flan,
        "f_debug":c_flan_debug
    }
}
