import re
import testing
import datetime as dt

re_fecha_anio = re.compile('\d{1,2}/\d{1,2}/\d{4}')     # dd/mm/aaaa            1/2/1995 3/12/2005 40/0/2020
re_fecha = re.compile('\d{1,2}/\d{1,2}')                # dd/mm                 1/2 10/6 5/15 20/20
re_dias = re.compile('\w{2}-\w{2}')                     # d1-d2                 ma-vi ju-ma
re_dia = re.compile('\w{2}')                            # di
re_hora = re.compile('\d{1,2}:\d{1,2}')                 # hh:mm

canales = {}

eventos = [
    {   "nombre":"ABRIR LA NORIEGA",
        "cuando":{"dia":"lu-vi", "hora":"9:00"},
        "accion":
        {   "tipo":"CH_PERM",
            "canal": testing.id_canal_noriega,
            "valor": True,
        }
    },
    {   "nombre":"CERRAR LA NORIEGA",
        "cuando":{"dia":"lu-vi", "hora":"18:00"},
        "accion":
        {   "tipo":"CH_PERM",
            "canal": testing.id_canal_noriega,
            "valor": False
        }
    },
    {   "nombre":"AVISO NORIEGA",
        "cuando":{"dia":"lu-vi", "hora":"17:55"},
        "accion":
        {   "tipo":"CH_MSG",
            "canal": testing.id_canal_noriega,
            "valor": "Atención: En 5 mimitos se cierra la Noriega"
        }
    },
    {   "nombre":"BUEN FINDE",
        "cuando":{"dia":"vi", "hora":"21:00"},
        "accion":
        {   "tipo":"CH_MSG",
            "canal": testing.id_canal_general,
            "valor": "Buen finde"
        }
    }
]

dias = ["lu","ma","mi","ju","vi","sa","do"]

def formato(s, r):
    return r.match(s)

def corresponde_dia(dia, actual):
    if dia == "siempre":
        return True
    if formato(dia, re_fecha_anio):
        d1 = dia.find("/")
        d2 = dia.find("/", d1+1)
        anio = dia[d2+1:]
        mes = dia[d1+1:d2]
        dia = dia[:d1]
        return actual == dt.date(year=int(anio), month=int(mes), day=int(dia))
    if formato(dia, re_fecha):
        return actual == actual.replace(day=int(dia[:dia.find("/")]), month=int(dia[dia.find("/")+1:]))
    if formato(dia, re_dias):
        d1 = dias.index(dia[:2])
        d2 = dias.index(dia[3:])
        if d2 > d1:
            return actual.weekday() >= d1 and actual.weekday() <= d2
        else:
            return actual.weekday() >= d1 or actual.weekday() <= d2
    if formato(dia, re_dia):
        return actual.weekday() == dias.index(dia)
    return False

def corresponde_hora(hora, actual):
    if formato(hora, re_hora):
        dp = hora.find(":")
        minutos = hora[dp+1:]
        hora = hora[:dp]
        return actual == dt.time(hour=int(hora), minute=int(minutos))
    return False

def corresponde(cuando):
    hoy = dt.datetime.now()
    if corresponde_dia(cuando["dia"], hoy.date()):
        if corresponde_hora(cuando["hora"], hoy.time().replace(second=0, microsecond=0)):
            return True
    return False

async def realizar(accion):
    canal = canales[accion["canal"]]
    if (canal):
        servidor = canal[0]
        canal = canal[1]
        if (accion["tipo"] == "CH_MSG"):
            await canal.send(accion["valor"])
        elif (accion["tipo"] == "CH_PERM"):
            await canal.set_permissions(servidor.default_role, send_messages=accion["valor"])

async def acciones_programadas():
    for evento in eventos:
        if corresponde(evento["cuando"]):
            await realizar(evento["accion"])

async def conectar(cliente):
    for guild in cliente.guilds:
        for c in guild.channels:
            canales[c.id] = [guild,c]
