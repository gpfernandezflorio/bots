import json
import os
import testing

from canales import nombreCanal
from calendario import data_fecha

ARCHIVO_EVENTOS = "eventos.json"
lista_de_eventos = []

def inicializar_eventos():
    global lista_de_eventos
    lista_de_eventos = []
    if os.path.isfile(ARCHIVO_EVENTOS):
        f = open(ARCHIVO_EVENTOS, 'r');
        lista_de_eventos = json.loads(f.read()) + eventos_hc
    else:
        f = open(ARCHIVO_EVENTOS, 'w')
        f.write(json.dumps([]))
        lista_de_eventos = eventos_hc
    f.close()

def listar_eventos():
    return lista_de_eventos

def data_evento(evento):
    txt = evento["nombre"]
    txt += "\n Estado: " + ("Habilitado" if evento.get("habilitado", False) else "Deshabilitado")
    txt += "\n Acción: " + data_accion(evento.get("accion", {"tipo":"NADA"}))
    txt += "\n Cuando: " + data_fecha(evento.get("cuando", {"dia":"-"}))
    return txt

def data_accion(accion):
    tipo = accion.get("tipo", "NADA")
    if tipo == "CH_PERM":
        canal = accion.get("canal")
        if canal is None:
            canal = "de un canal"
        else:
            canal = "del canal " + nombreCanal(canal)
        valor = accion.get("valor", False)
        return ("Habilitar" if valor else "Deshabilitar") + " permisos " + canal
    if tipo == "CH_MSG":
        msg = accion.get("valor")
        if msg is None:
            msg = "un mensaje"
        else:
            msg = "el mensaje \"" + msg + "\""
        canal = accion.get("canal")
        if canal is None:
            canal = ""
        else:
            canal = " al canal " + nombreCanal(canal)
        return "Mandar " + msg + canal
    return "Nada"

eventos_hc = [
    {   "nombre":"ABRIR_LA_NORIEGA",
        "cuando":{"dia":"lu-vi", "hora":"09:30"},
        "habilitado":True,
        "accion":
        {   "tipo":"CH_PERM",
            "canal": testing.id_canal_noriega,
            "valor": True,
        }
    },
    {   "nombre":"CERRAR_LA_NORIEGA",
        "cuando":{"dia":"lu-vi", "hora":"18:00"},
        "habilitado":True,
        "accion":
        {   "tipo":"CH_PERM",
            "canal": testing.id_canal_noriega,
            "valor": False
        }
    },
    {   "nombre":"AVISO_NORIEGA",
        "cuando":{"dia":"lu-vi", "hora":"17:55"},
        "habilitado":False,
        "accion":
        {   "tipo":"CH_MSG",
            "canal": testing.id_canal_noriega,
            "valor": "Atención: En 5 mimitos se cierra la Noriega"
        }
    },
    {   "nombre":"BUEN_FINDE",
        "cuando":{"dia":"vi", "hora":"21:00"},
        "habilitado":True,
        "accion":
        {   "tipo":"CH_MSG",
            "canal": testing.id_canal_general,
            "grupo": testing.TG_GROUP,
            "valor": "Buen finde"
        }
    },
    {   "nombre":"RALONDARIO",
        "cuando":{"dia":"siempre", "hora":"08:30"},
        "habilitado":True,
        "accion":
        {   "tipo":"CH_MSG",
            "canal": testing.id_canal_recordatorios,
            "grupo": -1001553265480,#testing.TG_GROUP,
            "funcion": "eventos_del_dia"
        }
    },
    {   "nombre":"TESIS",
        "cuando":{"dia":"siempre", "hora":"09:00"},
        "habilitado":True,
        "accion":
        {   "tipo":"CH_FILE",
            "canal": testing.id_canal_recordatorios,
            "grupo": testing.TG_GROUP,
            "funcion": "anuncio_proxima_tesis"
        }
    }
]
