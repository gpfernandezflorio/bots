import os
import json
import requests
import testing

URL = "https://api.telegram.org/bot" + testing.TG_TOKEN + "/"

ultimo_mensaje_fue_una_pregunta = {}

def inicializar():
  pass

def mandar_texto_revisando_ultimo_mensaje(chat_id, texto, respuesta_a=None):
    if (ultimo_mensaje_fue_una_pregunta.get(chat_id, False)):
        mandar_texto(chat_id, 'Lamento que nadie haya podido responderte pero tengo algo que decir.')
    mandar_texto(chat_id, texto, respuesta_a)

def mandar_texto(chat_id, texto, respuesta_a=None):
    print("SEND")
    #Llamar el metodo sendMessage del bot, passando el texto y la id del chat
    requests.get(URL + "sendMessage?text=" + texto + "&chat_id=" + str(chat_id) + "&reply_to_message_id=" + str(respuesta_a))

def mandar_archivo(chat_id, ruta, respuesta_a=None):
    files = {
      'photo': open(ruta, 'rb')
    }
    requests.post(URL + "sendPhoto?chat_id=" + str(chat_id) + "&reply_to_message_id=" + str(respuesta_a), files = files)

def recibir_mensajes():
    global ultimo_mensaje_fue_una_pregunta
    ultima_actualizacion = -1
    if os.path.exists("last_update.txt"):
      f = open("last_update.txt", 'r')
      line = f.readline()
      f.close()
      ultima_actualizacion = int(line.strip(' \t\r\n'))
    #Llamar al metodo getUpdates del bot, utilizando un offset
    respuesta = requests.get(URL + "getUpdates" + "?offset=" + str(ultima_actualizacion+1))
    #Telegram devolvera todos los mensajes con id IGUAL o SUPERIOR al offset

    #Decodificar la respuesta recibida a formato UTF8
    mensajes_js = respuesta.content.decode("utf8")

    #Convertir el string de JSON a un diccionario de Python
    mensajes_diccionario = json.loads(mensajes_js)

    if not ('result' in mensajes_diccionario):
        return []
    mensajes = mensajes_diccionario["result"]

    # Para que no me falle el update
    if len(mensajes) == 0:
      return []

    f = open("last_update.txt", 'w')
    f.write(str(mensajes[-1]['update_id']) + '\n')
    f.close()

    if (ultima_actualizacion == -1): # Para evitar repetir mensajes
        return []

    # Sólo mensajes de texto
    mensajes = filter(lambda x: ('message' in x) and ('text' in x['message']), mensajes)
    if testing.modo_testing:
      # Sólo mensajes del grupo de test
      mensajes = filter(lambda x: x["message"]["chat"]["id"]==testing.TG_GROUP, mensajes)
    mensajes = list(map(lambda x:
      # Devuelvo los mensajes con la siguiente representación
      {"texto":x["message"]["text"], "chat_id":x["message"]["chat"]["id"], "msg_id":x["message"]["message_id"]},
      mensajes))
    for msg in mensajes:
        ultimo_mensaje_fue_una_pregunta[msg['chat_id']] = msg['texto'].endswith('?')
    return mensajes
