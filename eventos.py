import json
import os
import testing

ARCHIVO_EVENTOS = "eventos.json"

def inicializar_eventos():
    eventos = []
    if os.path.isfile(ARCHIVO_EVENTOS):
        f = open(ARCHIVO_EVENTOS, 'r');
        eventos = json.loads(f.read())
        pass
    else:
        eventos = eventos_hc
        f = open(ARCHIVO_EVENTOS, 'w')
        f.write(json.dumps(eventos))
    f.close()
    return eventos

eventos_hc = [
    {   "nombre":"ABRIR LA NORIEGA",
        "cuando":{"dia":"lu-vi", "hora":"9:00"},
        "habilitado":True,
        "accion":
        {   "tipo":"CH_PERM",
            "canal": testing.id_canal_noriega,
            "valor": True,
        }
    },
    {   "nombre":"CERRAR LA NORIEGA",
        "cuando":{"dia":"lu-vi", "hora":"18:00"},
        "habilitado":True,
        "accion":
        {   "tipo":"CH_PERM",
            "canal": testing.id_canal_noriega,
            "valor": False
        }
    },
    {   "nombre":"AVISO NORIEGA",
        "cuando":{"dia":"lu-vi", "hora":"17:55"},
        "habilitado":False,
        "accion":
        {   "tipo":"CH_MSG",
            "canal": testing.id_canal_noriega,
            "valor": "Atención: En 5 mimitos se cierra la Noriega"
        }
    },
    {   "nombre":"BUEN FINDE",
        "cuando":{"dia":"vi", "hora":"21:00"},
        "habilitado":True,
        "accion":
        {   "tipo":"CH_MSG",
            "canal": testing.id_canal_general,
            "valor": "Buen finde"
        }
    },
    {   "nombre":"RALONDARIO",
        "cuando":{"dia":"siempre", "hora":"9:00"},
        "habilitado":True,
        "accion":
        {   "tipo":"CH_MSG",
            "canal": testing.id_canal_recordatorios,
            "funcion": "proximos_eventos_ralondario"
        }
    }
]
