import datetime as dt
from pytz import timezone

def nueva_fecha(año, mes, dia):
    return dt.date(año, mes, dia)

def nueva_fecha_hora(año, mes, dia, horas, minutos):
    return dt.datetime(year=año, month=mes, day=dia, hour=horas, minute=minutos)

def nuevo_horario(horas, minutos):
    return dt.time(hour=horas, minute=minutos)

def delta_dias(d):
    return dt.timedelta(days=d)

def fecha_desde_str(txt):
    return dt.datetime.strptime(txt, '%Y-%m-%d').date()

def justo_ahora():
    return dt.datetime.now(tz=timezone('America/Buenos_Aires'))

def dia_de_hoy():
    ahora = justo_ahora()
    return nueva_fecha(ahora.year, ahora.month, ahora.day)
