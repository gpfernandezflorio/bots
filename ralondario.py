#!/usr/bin/python3
# -*- coding: utf-8 -*-

from calendarios import proximos_eventos
from calendario import formatear_fecha

ID = "e1qrrpdi9d2ki9ruibp9gno484"

def formatear_nombre(txt, descripcion):
  P = txt.split(' - ')
  if P[0] == 'Finales':
      if len(P) == 3:
          return P[2] + ' a la ' + P[1].lower() + ' de finales'
      elif len(P) == 2:
          return P[1] + ' a finales'
  elif P[0] == "FINALES":
      txt = "Exámenes finales"
      if len(P) > 1:
          txt += " (" + P[1].lower() + ")"
  elif P[0] in ['Verano','1C','2C'] and len(P) == 2:
      return formatear_evento_cuatrimestre(P[1], P[0])
  return txt

def formatear_evento_cuatrimestre(E, C):
    if C == '1C':
        C = "l primer cuatrimestre"
    elif C == '2C':
        C = "l segundo cuatrimestre"
    else:
        C = " " + C.lower()
    if ('encuestas' in E.lower()) or ('materias' in E.lower()) or ('cursada' in E.lower()):
        return E + ' de' + C
    if 'inscripción' in E.lower():
        return E + ' a' + C
    return C + " - " + E

def formatear_hora(txt):
  return txt[:5] + 'hs'

def proximos_eventos_ralondario(info={}):
  dias = info.get("dias", 7)
  cantidad = info.get("cantidad", 10)
  monospace = info.get("monospace", False)
  recortar_en = info.get("recortar_en", "ambos") # puede ser "dias", "cantidad" o "ambos"
  mensaje = info.get("titulo", None)
  if mensaje is None:
    if recortar_en == "dias":
      mensaje = "Eventos de los próximos " + str(dias) + " días:"
    elif recortar_en == "cantidad":
      mensaje = "Próximos " + str(cantidad) + " eventos:"
    else:
      mensaje = "Próximos eventos:"
  eventos = []
  for evento in proximos_eventos(ID, cantidad, dias, recortar_en):
    nombre = formatear_nombre(evento['summary'], evento.get('description',''))
    inicio = evento['start']
    fecha = formatear_fecha(inicio, monospace)
    hora = None
    texto = nombre
    if 'dateTime' in inicio:
      hora = formatear_hora(inicio['dateTime'][11:])
      texto += " a las " + hora
    if 'location' in evento:
      lugar = evento['location']
      texto += " en " + lugar
    eventos.append({"fecha":fecha,"texto":texto})
  fecha = ""
  if len(eventos) == 0:
      mensaje = None #"No tengo nada que reportar"
  elif dias == 0:
      mensaje = "Eventos del día:"
      fecha = eventos[0]["fecha"]
  if (monospace):
    for evento in eventos:
      if evento["fecha"] != fecha:
        fecha = evento["fecha"]
        mensaje += "\n" + fecha + ": " + evento["texto"]
      else:
        mensaje += "\n       " + evento["texto"]
  else:
    for evento in eventos:
      if evento["fecha"] != fecha:
        fecha = evento["fecha"]
        mensaje += "\n[[ " + fecha + " ]]"
      mensaje += "\n * " + evento["texto"]
  return mensaje

def proxima_tesis():
  res = []
  for evento in proximos_eventos(ID, 50, 0, "dias"):
    if evento['summary'].lower().startswith("defensa de tesis"):
      hora = ""
      inicio = evento['start']
      if 'dateTime' in inicio:
        hora = formatear_hora(inicio['dateTime'][11:16])
      res.append([evento['summary'][17:], hora])
  return res
