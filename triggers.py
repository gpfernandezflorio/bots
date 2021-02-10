import datetime as dt

H = 2 # Cantidad de horas entre un trigger y el siguiente

def procesar_mensaje(txt):
    for trigger in triggers:
        i = trigger["in"]
        if type(i) == type(""):
            res = activar_trigger(i, trigger, txt)
            if res["OK"]:
                return res["txt"]
        elif type(i) == type([]):
            for p in i:
                res = activar_trigger(p, trigger, txt)
                if res["OK"]:
                    return res["txt"]
    return None

def activar_trigger(i, trigger, txt):
    if i in txt.lower():
        if corresponde_mandarlo(trigger):
            o = trigger["out"]
            if type(o) == type(""):
                return {"OK":True, "txt":o}
            elif type(o) == type(lambda x: x):
                return {"OK":True, "txt":o(txt)}
        return {"OK":True, "txt":None} # trigger activado pero no corresponde
    return {"OK":False} # trigger no activado; seguir buscando

def corresponde_mandarlo(trigger):
    ahora = dt.datetime.now()
    ultimo_enviado = trigger.get("ts", None)
    if ultimo_enviado is None:
        trigger["ts"] = dt.datetime.now()
        return True
    trigger["ts"] = ahora # Actualizo aunque no lo tenga que mandar
    tiempoTranscurrido = ahora - ultimo_enviado
    return tiempoTranscurrido.total_seconds() > 3600*H

triggers = [
    {"in": 'q onda?', "out": 'q onda?'},
    {"in": ['felicitaciones','felicidades','felicito','feliz','congrats','congratulation'],
    "out": 'Felicitaciones Charly!'}
]
