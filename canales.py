todos_los_canales = {}

def obtener_canales():
    return todos_los_canales

def agregar_canal(guild, c):
    global todos_los_canales
    todos_los_canales[c.id] = [guild,c]

def obtener_canal(i):
    return todos_los_canales[i]

def nombreCanal(i):
    if i in todos_los_canales:
        return str(todos_los_canales[i][1])
    return str(i)
