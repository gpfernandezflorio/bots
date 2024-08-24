import os
from fechayhora import justo_ahora
from dotenv import load_dotenv

load_dotenv()
modo_testing = os.getenv('TEST_MODE')=="YES"
servidor = "TEST" if modo_testing else "DC"
id_admin = int(os.getenv('DISCORD_ADMIN'))
#print("ID ADMIN: " + str(id_admin))
id_me = int(os.getenv('DISCORD_ME'))
#print("ID ME: " + str(id_me))
id_servidor = int(os.getenv('DISCORD_GUILD_'+servidor))
#print("ID SERVIDOR: " + str(id_servidor))
id_rol = int(os.getenv('DISCORD_'+servidor+'_MY_ROLE'))
#print("ID ROL: " + str(id_rol))
id_canal_noriega = int(os.getenv('DISCORD_'+servidor+'_CH_NORIEGA'))
#print("ID CANAL NORIEGA: " + str(id_canal_noriega))
id_canal_general = int(os.getenv('DISCORD_'+servidor+'_CH_GENERAL'))
#print("ID CANAL GENERAL: " + str(id_canal_general))
id_canal_recordatorios = int(os.getenv('DISCORD_'+servidor+'_CH_RECORDATORIOS'))
#print("ID CANAL RECORDATORIOS: " + str(id_canal_recordatorios))
TG_TOKEN = os.getenv('TG_TOKEN')
TG_GROUP = int(os.getenv('TG_'+servidor+'_GROUP'))

ARCHIVO_LOG = 'log.txt'

def logTxt(m):
  msg = str(justo_ahora()) + " "
  if m.find('\n') < 0:
    msg += ' '
  else:
    msg += '\n'
  msg += m
  f = open(ARCHIVO_LOG, 'a')
  f.write(msg + "\n")
  f.close()

def logExcp(e, msg=None):
  m = mostrar_excepcion(e)
  if not (msg is None):
    m = msg + "\n" + m
  logTxt(m)

def mostrar_excepcion(e):
  res = ""
  tb = e.__traceback__
  while not (tb is None):
    res = "\n" + tb.tb_frame.f_code.co_filename + ":" + str(tb.tb_lineno) + " (" + tb.tb_frame.f_code.co_name + ")" + res
    tb = tb.tb_next
  return str(e).replace("<","&lt;").replace(">","&gt;") + res