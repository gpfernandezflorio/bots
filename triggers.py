from fechayhora import justo_ahora

H = 2 # Cantidad de horas entre un trigger y el siguiente

def procesar_mensaje(txt, grupo):
    for trigger in triggers:
        i = trigger["in"]
        if type(i) == type(""):
            res = activar_trigger(i in txt.lower(), trigger, txt, grupo)
            if res["OK"]:
                return res["txt"]
        elif type(i) == type([]):
            for p in i:
                res = activar_trigger(p in txt.lower(), trigger, txt, grupo)
                if res["OK"]:
                    return res["txt"]
        elif type(i) == type(lambda x : x):
            res = activar_trigger(i(txt), trigger, txt, grupo)
            if res["OK"]:
                return res["txt"]
    return None

def activar_trigger(c, trigger, txt, grupo):
    if c:
        if corresponde_mandarlo(trigger, grupo):
            o = trigger["out"]
            if type(o) == type(""):
                return {"OK":True, "txt":o}
            elif type(o) == type(lambda x: x):
                return {"OK":True, "txt":o(txt)}
        return {"OK":True, "txt":None} # trigger activado pero no corresponde
    return {"OK":False} # trigger no activado; seguir buscando

def corresponde_mandarlo(trigger, grupo):
    ahora = justo_ahora()
    ultimo_enviado = trigger.get("ts", None)
    if ultimo_enviado is None:
        trigger["ts"] = {}
        trigger["ts"][grupo] = ahora
        return True
    ultimo_enviado = ultimo_enviado.get(grupo, None)
    trigger["ts"][grupo] = ahora # Actualizo aunque no lo tenga que mandar
    if ultimo_enviado is None:
        return True
    tiempoTranscurrido = ahora - ultimo_enviado
    return tiempoTranscurrido.total_seconds() > 3600*H

def es_faq_nuevo_plan(txt):
    txt_lower = txt.lower()
    return 'plan' in txt_lower and ('nuevo' in txt_lower or 'cambio' in txt_lower)

def faqs_nuevo_plan(txt):
    return 'No te preocupes, no te vas a quedar sin poder cursar. Cada materia del plan viejo tiene equivalencia con alguna del plan nuevo. Además, no es obligatorio cambiarte de plan. Podés seguir cursando el plan viejo aunque curses materias del plan nuevo por equivalencia.\n\nMás información:\nhttps://docs.google.com/document/d/e/2PACX-1vSlD-djaJcnw45-41ugO5yGqNl5hA_dKOAikyRDAh5QzsrToBi2XWPzU1i0ldDAbNct0rx2AfhuBf19/pub'

triggers = [
    {"in": 'q onda?', "out": 'q onda?'},
    {"in": ['felicitaciones','felicidades','felicito','feliz','congrats','congratulation'],
        "out": 'Felicitaciones Charly!'},
    {"in": es_faq_nuevo_plan, "out": faqs_nuevo_plan}
]
