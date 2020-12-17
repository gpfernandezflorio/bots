import testing

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
