from calendarios import proximos_eventos
from calendario import formatear_fecha, corresponde
from fechayhora import fecha_desde_str, dia_de_hoy

ID = "sn0ir2b77hr77k7f1it9q2u730"

def menu_comedor(info={}):
    hoy = dia_de_hoy()
    if "fecha" in info:
        fecha = info["fecha"]
        mensaje = "Menú del " + str(fecha.day) + "/" + str(fecha.month) + ": "
        error = "No se encontró menú para el " + str(fecha.day) + "/" + str(fecha.month) + "."
    else:
        fecha = hoy
        mensaje = "Menú de hoy: "
        error = "No se encontró menú para hoy."
    n = 1 + (fecha - hoy).days
    for evento in proximos_eventos(ID, n, n, "dias"):
        fecha_evento = fecha_desde_str(evento['start']['date'])
        if fecha == fecha_evento:
            return mensaje + evento['summary']
    return error
