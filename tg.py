import os
import testing
import twx.botapi as tb

bot = tb.TelegramBot(testing.TG_TOKEN)

def inicializar():
    bot.update_bot_info().wait()

def mandar_texto(chat_id, texto, respuesta_a=None):
    bot.send_message(chat_id, texto, reply_to_message_id=respuesta_a)

def mandar_archivo(chat_id, ruta, respuesta_a=None):
    fp = open(ruta, 'rb')
    file_info = tb.InputFileInfo(ruta, fp, 'image/png')
    bot.send_photo(chat_id, photo=tb.InputFile('photo', file_info), reply_to_message_id=respuesta_a)

def recibir_mensajes():
  ultima_actualizacion = -1
  if os.path.exists("last_update.txt"):
    f = open("last_update.txt", 'r')
    line = f.readline()
    f.close()
    ultima_actualizacion = int(line.strip(' \t\r\n'))
  actualizaciones = bot.get_updates(offset=ultima_actualizacion + 1).wait()
  if (actualizaciones is None) or (len(actualizaciones)==0):
    return []
  f = open("last_update.txt", 'w')
  f.write(str(actualizaciones[-1].update_id) + '\n')
  f.close()
  actualizaciones_con_mensajes = filter(lambda x: not (x.message is None) and not (x.message.text is None), actualizaciones)
  mensajes = map(lambda x:
    # Devuelvo lo mensajes con la siguiente representación
    {"texto":x.message.text, "chat_id":x.message.chat.id, "msg_id":x.message.message_id},
    actualizaciones_con_mensajes)
  return mensajes
