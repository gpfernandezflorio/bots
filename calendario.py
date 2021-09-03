import re
import datetime as dt

re_fecha_año = re.compile('\d{1,2}/\d{1,2}/\d{4}')      # dd/mm/aaaa            1/2/1995 3/12/2005 40/0/2020
re_fecha = re.compile('\d{1,2}/\d{1,2}')                # dd/mm                 1/2 10/6 5/15 20/20
re_dias = re.compile('\w{2}-\w{2}')                     # d1-d2                 ma-vi ju-ma
re_dia = re.compile('\w{2}')                            # di
re_hora = re.compile('\d{1,2}:\d{1,2}')                 # hh:mm

dias = ["lu","ma","mi","ju","vi","sa","do"]
nombre_dias = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
nombres_meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]

def data_fecha(fecha):
    dia = fecha.get("dia", "-")
    hora = fecha.get("hora")
    if hora is None:
        hora = ""
    else:
        hora = " a las " + hora
    if (dia == "siempre"):
        dia = "Todos los días"
    elif formato(dia, re_fecha_año):
        dia = dia.split("/")
        dia = "El " + dia[0] + " de " + nombres_meses[int(dia[1])-1] + " de " + dia[2]
    elif formato(dia, re_fecha):
        dia = dia.split("/")
        dia = "Todos los " + dia[0] + " de " + nombres_meses[int(dia[1])-1]
    elif formato(dia, re_dias):
        dia = "De " + nombre_dias[dias.index(dia[:2])] + " a " + nombre_dias[dias.index(dia[3:])]
    elif formato(dia, re_dia):
        dia = "Los " + nombre_dias[dias.index(dia)]
        if not dia.endswith("s"):
            dia += "s"
    else:
        dia = "Nunca"
    return dia + hora

def formato(s, r):
    return r.match(s)

def calcular_hora(hora):
    if formato(hora, re_hora):
        dp = hora.find(":")
        minutos = hora[dp+1:]
        hora = hora[:dp]
        return dt.time(hour=int(hora), minute=int(minutos))
    return None

def calcular_fecha(dia, desde, hora):
    if dia == "siempre":
        return desde.replace(hour=hora.hour, minute=hora.minute)
    if formato(dia, re_fecha_año):
        d1 = dia.find("/")
        d2 = dia.find("/", d1+1)
        año = dia[d2+1:]
        mes = dia[d1+1:d2]
        dia = dia[:d1]
        resultado = dt.datetime(year=int(año), month=int(mes), day=int(dia), hour=hora.hour, minute=hora.minute)
        if resultado < desde:
            return None
        return resultado
    if formato(dia, re_fecha):
        resultado = desde.replace(day=int(dia[:dia.find("/")]), month=int(dia[dia.find("/")+1:]), hour=hora.hour, minute=hora.minute)
        if resultado < desde:
            resultado = resultado.replace(year=resultado.year + 1)
        return resultado
    if formato(dia, re_dias):
        d1 = dias.index(dia[:2])
        d2 = dias.index(dia[3:])
        hoy = desde.weekday()
        if d2 > d1:
            while(hoy < d1 or hoy > d2):
                hoy = (hoy+1)%7
        else:
            while(hoy < d1 and hoy > d2):
                hoy = (hoy+1)%7
        delta = (hoy - desde.weekday()) % 7
        return desde.replace(hour=hora.hour, minute=hora.minute) + dt.timedelta(days=delta)
    if formato(dia, re_dia):
        delta = (dias.index(dia) - desde.weekday()) % 7
        return desde.replace(hour=hora.hour, minute=hora.minute) + dt.timedelta(days=delta)
    return None

def crear_fecha(cuando, hoy):
    hora = calcular_hora(cuando["hora"])
    if (hora is None):
        return None
    # Me fijo si hoy ya pasó
    if hora < hoy.time():
        return calcular_fecha(cuando["dia"], hoy + dt.timedelta(days=1), hora)
    return calcular_fecha(cuando["dia"], hoy, hora)

def obtener_eventos_siguientes(lista_de_eventos):
    hoy = dt.datetime.now().replace(second=0, microsecond=0)
    proxima_fecha = None
    eventos = []
    for evento in lista_de_eventos:
        if evento["habilitado"]:
            fecha_evento = crear_fecha(evento["cuando"], hoy)
            if (proxima_fecha is None):
                proxima_fecha = fecha_evento
                eventos = [evento]
            elif fecha_evento < proxima_fecha:
                proxima_fecha = fecha_evento
                eventos = [evento]
            elif fecha_evento == proxima_fecha:
                eventos.append(evento)
    print("NEXT: " + str(proxima_fecha))
    for evento in eventos:
        print(" * " + evento["nombre"])
    return [proxima_fecha] + eventos

def corresponde(cuando):
    hoy = dt.datetime.now().replace(second=0, microsecond=0)
    return cuando == hoy

def formatear_fecha(txt, monospace=False):
  if 'date' in txt:
      txt = txt['date']
  elif 'dateTime' in txt:
      txt = txt['dateTime'][:10]
  else:
      return ''
  dia_n = 0
  mes_n = 0
  dia_s = ''
  mes_s = ''
  if (monospace):
    if txt[8] == "0":
      txt = txt[:8] + " " + txt[9:]
    if txt[5] == "0":
      txt = txt[:5] + txt[6] + " " + txt[7:]
    dia_s = txt[8:10]
    mes_s = txt[5:7]
    dia_n = int(dia_s)
    mes_n = int(mes_s)
  else:
    dia_n = int(txt[8:10])
    mes_n = int(txt[5:7])
    dia_s = str(dia_n)
    mes_s = str(mes_n)
  hoy = dt.date.today()
  if (hoy.day == dia_n and hoy.month == mes_n):
    return "HOY"
  fecha = dt.datetime.strptime(txt, '%Y-%m-%d').date()
  if (fecha == hoy + dt.timedelta(days=1)):
    return "Mañana"
  return "El " + nombre_dias[fecha.weekday()] + " " + dia_s + "/" + mes_s
