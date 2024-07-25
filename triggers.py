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
    return '¿Tenés dudas sobre el cambio de plan?\nRevisá las FAQs de CubaWiki:\nhttps://www.cubawiki.com.ar/index.php/Faq/cursada/plan'

triggers = [
    {"in": 'q onda?', "out": 'q onda?'},
    {"in": ['felicitaciones','felicidades','felicito','feliz','congrats','congratulation'],
        "out": 'Felicitaciones Charly!'},
    {"in": es_faq_nuevo_plan, "out": faqs_nuevo_plan},
    {"in": 'dalu', "out": "La dirección de Estudiantes y graduados (dalu) atiende de 12 a 18. También podés mandarles mail a dalu@de.fcen.uba.ar."},
    {"in": 'gracias tina', "out": "Es \"tina gracias\"."},
    {"in": ['wifi','wi-fi','wi fi'],
      "out": "En el pabellón cero casi nunca anda el wi-fi pero acá tenés algunas opciones:\n\n*Red*:EVENTO\n*Contraseña*:UBA-2022\n\n*Red*:Comedor\n*Contraseña*:UBA1865!\n\n*Red*:UBA-WiFi\nEsta red es pública pero para tener conexión tenés que iniciar sesión con tu usuario de la UBA. Si todavía no lo creaste podés hacerlo desde https://wifi.uba.ar/ (habiéndote conectado a la red)."},
    {"in": ['secretaria','secretaría'],
      "out": "La secretaría del DC atiende en la oficina 1502 del pabellón 0 de 13 a 20. No atienden por mail pero podés comunicarte abriendo un ticket en https://secretaria.dc.uba.ar/."}
]
