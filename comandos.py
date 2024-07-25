import testing
from eventos import listar_eventos, data_evento
from ralondario import proximos_eventos_ralondario
from comedor import menu_comedor
from canales import obtener_canal
from fechayhora import dia_de_hoy, nueva_fecha
import tg
import discord
# import imageDraw

urlPlanos = {
  '0':{
    'pb':'https://drive.google.com/file/d/1Z3j_ykPwzqe48Rwt7p-jRvmjn3VGq16j/view?usp=share_link',
    '1':'https://drive.google.com/file/d/1-SVgAzbGiSD1uTnj2CIFAKGB3tJ5A4_C/view?usp=share_link'
    },
  '1':{
    'pb':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2020/02/PI_PB_HYS-A4.pdf',
    '1':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2022/08/PI_1oP-A3.pdf',
    '2':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2020/02/PI_2%C2%BAP_HYS-A4.pdf'
    },
  '2':{
    'ss':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2020/02/PII_SS-A4.pdf',
    'es':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2022/08/PII_ES-A3.pdf',
    'pb':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2020/02/PII_PB-A4-1.pdf',
    '1':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2020/02/PII_1%C2%BAP-A4.pdf',
    'ep':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2020/02/PII_EP-A4-1.pdf',
    '2':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2020/02/PII_2%C2%BAP-A4.pdf',
    '3':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2020/02/PII_3%C2%BAP-A4.pdf',
    '4':'https://exactas.uba.ar/higieneyseguridad/wp-content/uploads/2020/02/PII_4%C2%BAP-A4.pdf'
    }
}

gps = {
  '0':{
    'pb':{'Aula':['1101 (Seminario)','1102','1103','1104','1105','1106','1107','1108','1109',
            '1110','1111','1112','1113','1114','1115',
            '1203','1204','1205','1206','1207','1208','1209',
            '1301','1302','1303','1304','1305','1306','1307','1308','1309 (Seminario)',
            '1401 (Seminario)','1402 (Seminario)','1403 (Seminario)'],
          'Laboratorio':['de Robótica (1506)'],
          'Secretaría':['de Computación (1502)','Técnica (1505)','de Extensión DC (1508)'],
          'Sala':['de Control Alarma y Afines (1202)','de Proyectos (1501)','de Proyectos (1504)',
            'de servidores / cluster (1602)','Administración de Sistemas (1603)','de Reuniones (1604)',
            'de lectura (1605)','de Reuniones (1606)'],
          '_':['SST (1201)','Kiosco Polirubro (1210)','Kiosco CECEN (1503)','Cafetería',
            'ICC (1507)','Bedelía (1601)']
    },
    '1':{'Oficina':['2102','2106','2107','2108','2109','2110','2111','2112','2113','2114','2115','2116','2117','2118',
           '2200','2201','2202','Director Científico (2206)','Director Adm. (2207)',
           '2300','2301','2302','2303','2304','2305','2306','2307','Director I.C.Atm. (2400)',
           'C.A.M. Meteorología (2404)','DIAIFCC (Cambio Climático) (2405)','2406','2407','2408',
           '2500','2501','2502','2503','2504','2505','2506','2507','2508','2509',
           '2510','2511','2512','2513','2514','2515','2516','2517','2518','2519',
           '2520','2521','2522','2523','2524','2525','2526','2527','2528','2529',
           '2530','2531',
           '2600','2601','2602','2603','2604','2605','2606','2607','2608','2609',
           '2610','2611','2612','2613','2614','2615','2616','2617','2618','2619',
           '2620','2621','2622','2623'],
         'Secretaría':['de Computación (2103)','Acedémica I.C.Atm. (2402)'],
         'Sala':['de Reuniones (2101)','de lectura (2119)','de Reuniones I.C.Atm. (2308)','de Profesores I.C.Atm (2403)'],
         '_':['Admin. Alumnos de grado de Comp. (2104)','Admin. Alumnos de posgrado de Comp. (2105)',
           'Puestos Flexibles (2203)','Sector de Reuniones (2204)','Secretaría (2205)',
           'Recepción y Secretaría I.C.Atm. (2401)','STC/SUMIC Atm. (2409)','STC/SUMIC Atm. (2410)','Cocina']
    }
  },
  '1':{
    'pb':{'Aula':['Seminario'],
          'Laboratorio':['1','2','3','4','5','6','Epsilon',
            'B27','B28','B30','B31','B32','B33','B34','B35','B36','B37','B38','B39','B41','B42','B43',
            'de Sistemas Complejos','Líquidos Criogénicos','de Bajas Temperaturas','Serv. de Elect.',
            'Física Aplicada 1','Física Aplicada 2','Física Aplicada 3','Física Aplicada 4',
            'Emprendimientos 1','Emprendimientos 2','Emprendimientos 3 A','Emprendimientos 3 B',
            'Física del Plasma','de Tecnología de Plasma'],
          'Sala':['de servidores','de cluster','de reunión'],
          'Taller':['de tornería'],
          '_':['Cuarto','Secretaría','Adm. de redes','Depósito','Bar Comedor','Intendencia',
            'Fotocopiadora']
    },
    '1':{'Aula':['Magna','2','3','4','5','6','7','8','9','P. Federman'],
         'Laboratorio':['3','4','5','de Ondas','de Bajas Temperaturas','de Resonancia Magnética Nuclear',
           'de Mecánica Elemental','de Fotónica','de Neurociencia Integrativa','de Procesamiento de Imágenes',
           'de Sistemas Dinámicos','de Microscopia y Microespectoscopia','de Elect. Cuántica','de Láser Lec',
           'de Elect. Lec','de Polímeros Materiales Compuestos'],
         'Cuarto':['1','2','3','4'],
         'Sala':['estudios'],
         'Biblioteca':['LEC'],
         '_':['Bedelía','TTVE','Centro de Microscopias Avanzadas']
    },
    '2':{'Aula':['Seminario'],
         'Laboratorio':['de Computación A','de Computación B','de Electricidad y Magnetismo'],
         'Cuarto':['1','2','3','4','5','6','7','8','9','10'],
         'Oficina':['2018','2020','2022','2032','2034','2036','2038','2046','2054','2056','2058',
            '2060','2063','2065','2067','2069','2071','2073','2075','2077','2079',
            '2082','2083','2084','2085','2086','2087','2088','2089',
            '2090','2091','2092','2093','2094','2095','2096','2097','2098','2099',
            '2100','2102','2103','2104','2105','2106','2107','2108',
            '2113','2114','2115','2116','2117','2118','2119',
            '2120','2121','2122','2123','2124','2125','2126','2127','2128','2129',
            '2134','2135','2136','2137','2138','2139',
            '2140','2142','2144','2146',
            '2150','2151','2152','2153','2154','2155','2156','2157','2159',
            '2160','2161','2162','2163','2164','2165','2166','2167',
            '2172','2173','2174','2175','2176','2177','2178','2179'],
          'Secretaría':['de Matemática','de Física'],
          'Dirección':['Matemática','Física'],
          'Sala':['de reuniones Matemática','de reuniones Computación','de lectura','Hubs'],
          'Biblioteca':['UMA','R.Pastor'],
          '_':['Pecera','Cluster','Mantenimiento de redes','Cocina','Hemeroteca']
    }
  },
  '2':{
    'ss':{'Aula':['Magna'],
          'Laboratorio':['IGEBA','Foto','Neurobiología de la Memoria','Mosquitos'],
          'Estudio':['1','2'],
          'Sala':['de Transf','de Celdas y Tab. Generales','de Máquinas'],
          'Taller':['Carpintería','Mecánica / Herrería'],
          'Depósito':['Ecología Genética y Evolución','BBE','Bar','Geología','Suministros'],
          '_':['Talleres','DIR','Elemento de vidrios','Electrotecnia','UMYMFOR',
            'Instituto Antártico CIBEA','Archivo','Servicios Impresión','Programa Historia FCEyN',
            'Consultorio','Telefonía','Depósito','Suministros','Área de Campaña (EGE)','Mantenimiento',
            'Sec. de Mantenimiento','Droguero General','Droguero Orgánico','Residuos Patogénicos','Residuos Peligrosos',
            'Seguridad y Control']
    },
    'es':{'Aula':['Magna','01','02','03','04','05','06','07','08','09','10'],
          'Laboratorio':['11','12','13','14','15','16','17','18','19','20'],
          'Sala':['de reuniones','de espera'],
          'Subsecretaría':['de Comunicación'],
          '_':['Herbario','E.P. Carpintería','E.P. Mecánica','Fotografía','Edición','Diseño']
    },
    'pb':{'Aula':['Seminario','11','12','13','15'],
          'Secretaría':['Privada','General','de Hacienda','Académica','de Posgrado','de Extensión'],
          'Subsecretaría':['Técnica','de Relaciones Interinstitucionales'],
          'Dirección':['Mesa Entrada','Asuntos Jurídicos','General Administrativa','de Movimientos de Fondos',
            'de Personal','de Alumnos y Graduados'],
          'Departamento':['Concursos Docentes','de Compras'],
          'Sala':['Espera','Jurado','de Reuniones'],
          'Depósito':['Hábitat','Economato'],
          '_':['Decanato','Consejo Directivo','Fotocopias','Kiosco','Librería','SUM CECEN','Bedelía','Info',
            'SUM','Gremial Docente','UTI','Servicio de Higiene y Seguridad','Correo Interno','APUBA','EUDEBA',
            'Admin. CECEN','Informática','Bar CECEN','Recepción','DOV','Despacho','Deportes','Cultura y Bienestar',
            'Pasantías','Servicios Generales','Entrevistas','Salón Roberto Arlt','Bar Comedor','Jardín Maternal',
            'Dirección','Contable','Tesorería','Inv. Cient. y Tecnológica General','Sumarios','UVA','Seguridad y Control',
            'Comedor Jardín','Cocina']
    },
    '1':{'Aula':['A','B','C',
           '1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19',
           '20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','39',
           '40','41','42','43','44','45','46','47','48','49','51','52','53','54','55','56','57','58','59',
           '60','61','62','63',
           'P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15','P16','P17','P18',
           'P20','P21','P23','P24','P25','P26','P28','P30','P31','P32'],
         'Secretaría':['de Geología','de Química Inorgánica'],
         'Departamento':['de Geología'],
         'Sala':['Silenciosa','Parlante'],
         'Biblioteca':['Le Loir'],
         '_':['Sedimentología','Volcanes Activos','Museo Mineral','Geología Histórica','Paleontología','Gimnasio',
           'INQUIMAE','Dirección','Fotocopiadora','Gimnasio']
    },
    'ep':{},
    '2':{},
    '3':{},
    '4':{}
  }
}

urlFlan = 'https://www.cubawiki.com.ar/images/a/a0/Plandeestudios.png'
fileFlan = "files/flan.png"
fileFlanLCD = "files/flan_lcd.png"

def es_para_mi(msg):
    comando = None
    if msg.startswith("<@!"+str(testing.id_me)+">") or msg.startswith("<@&"+str(testing.id_rol)+">"):
        comando = msg[msg.find('>')+1:]
    elif msg[:4].lower() == "tina":
        comando = msg[4:]
    elif msg[:5].lower() == "@tina":
        comando = msg[5:]
    elif msg[:13].lower() == "@mar_tina_bot":
        comando = msg[13:]
    if not (comando is None):
        while len(comando) > 0 and comando[0] == ' ':
            comando = comando[1:]
        if len(comando) == 0:
            return None
        return comando
    return None

def recibir_comando(msg):
  info_comando = {"OK":False}
  comando = es_para_mi(msg)
  if comando is None:
      return info_comando
  delimitador = comando.find(' ')
  argumentos = []
  if delimitador > 0:
      argumentos = comando[delimitador+1:]
      while len(argumentos) > 0 and argumentos[0] == ' ':
          argumentos = argumentos[1:]
      if len(argumentos) == 0:
        argumentos = []
      else:
        argumentos = argumentos.split(' ');
      comando = comando[:delimitador]
  info_comando["comando"] = comando
  info_comando["argumentos"] = argumentos
  info_comando["OK"] = True
  return info_comando

async def ejecutar_comando_discord(comando, argumentos, msg):
    if (comando in comandos_validos):
        await comandos_validos[comando]['f_discord'](argumentos, msg)

def ejecutar_comando_telegram(comando, argumentos, msg):
    if (comando in comandos_validos):
        comandos_validos[comando]['f_telegram'](argumentos, msg)

def ejecutar_comando_debug(comando, argumentos, msg):
    if (comando in comandos_validos):
        comandos_validos[comando]['f_debug'](argumentos, msg)

async def c_flan_discord(args, msg):
    if len(args) == 0 or (len(args) > 0 and args[0] == 'n'):
        await msg.channel.send(file=discord.File(fileFlan))
    elif len(args) > 0 and args[0] == 'v':
        await msg.channel.send(urlFlan)
    elif len(args) > 0 and args[0] == 'd':
        await msg.channel.send(file=discord.File(fileFlanLCD))

def c_flan_telegram(args, msg):
    if len(args) == 0 or (len(args) > 0 and args[0] == 'n'):
        tg.mandar_archivo(msg["chat_id"], fileFlan)
    elif len(args) > 0 and args[0] == 'v':
        tg.mandar_texto(msg["chat_id"], urlFlan, msg["msg_id"])
    elif len(args) > 0 and args[0] == 'd':
        tg.mandar_archivo(msg["chat_id"], fileFlanLCD)

def c_flan_debug(args, msg):
    if len(args) == 0 or (len(args) > 0 and args[0] == 'n'):
        print(fileFlan)
    elif len(args) > 0 and args[0] == 'v':
        print(urlFlan)
    elif len(args) > 0 and args[0] == 'd':
        print(fileFlanLCD)

def recordatorios(args):
    txt = "Lista de tareas:"
    if len(args) == 0:
        for evento in listar_eventos():
            txt += "\n " + evento["nombre"]
    else:
        nombre = args[0]
        for evento in listar_eventos():
            if evento["nombre"] == nombre:
                return data_evento(evento)
        txt = "Tarea inexistente: " + nombre
    return txt

async def c_recordatorios_discord(args, msg):
    await msg.channel.send(recordatorios(args))

def c_recordatorios_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], recordatorios(args), msg["msg_id"])

def c_recordatorios_debug(args, msg):
    print(recordatorios(args))

origenes = [
    {
        'claves': ['cubawiki'],
        'rta': "CUBA = Computación UBA\n\nO sea.. es meme, pero tiene sentido.\n\nBah, es un mix de eso y el chiste de q son cosas comunitarias de la gente de la carrera para gente de la carrera :)"
    },
    {
        'claves': ['flan'],
        'rta': "Porque se parece a \"plan\"."
    },
    {
        'claves': ['dalu'],
        'rta': "Porque originalmente se llamaba \"Departamento de ALUmnos\". D + ALU = DALU."
        }
]

def porque(args):
    if len(args) == 0:
        return "Tenés que pasarme como argumento aquello sobre lo que querés saber el origen."
    clave = args[0].lower()
    for o in origenes:
        if clave in o['claves']:
            return o['rta']
    return "No conozco el origen de eso."

def man(args):
    txt = "Lista de comandos:"
    if len(args) == 0:
        for comando in comandos_validos.keys():
            if not ('hidden' in comandos_validos[comando]):
                txt += "\n " + comando + " - " + comandos_validos[comando]["ayuda"][0]
    else:
        nombre = args[0]
        if nombre in comandos_validos:
            return "[[" + nombre + "]]\n" + comandos_validos[nombre]["ayuda"][1]
        txt = "Comando inexistente: " + nombre
    return txt

async def c_porque_discord(args, msg):
    await msg.channel.send(porque(args))

def c_porque_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], porque(args), msg["msg_id"])

def c_porque_debug(args, msg):
    print(porque(args))

async def c_man_discord(args, msg):
    await msg.channel.send(man(args))

def c_man_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], man(args), msg["msg_id"])

def c_man_debug(args, msg):
    print(man(args))

async def c_horarios_discord(args, msg):
    await msg.channel.send("https://docs.google.com/spreadsheets/d/1x3ji1bgcWlV14BY5x-KYttg140PshUv6RpJzPdFh8MA")

def c_horarios_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], "https://docs.google.com/spreadsheets/d/1x3ji1bgcWlV14BY5x-KYttg140PshUv6RpJzPdFh8MA", msg["msg_id"])

def c_horarios_debug(args, msg):
    print("https://docs.google.com/spreadsheets/d/1x3ji1bgcWlV14BY5x-KYttg140PshUv6RpJzPdFh8MA")

async def c_decir_discord(args, msg):
    if (len(args) < 2):
        await msg.channel.send("Faltan argumentos")
    else:
        print(args[0])
        channel = obtener_canal(int(args[0]))
        if (channel is None):
            await msg.channel.send("Id de canal inválido")
        else:
            print(channel)
            await channel[1].send(" ".join(args[1:]))

def c_decir_telegram(args, msg):
    if (len(args) < 2):
        tg.mandar_texto(msg["chat_id"], "Faltan argumentos", msg["msg_id"])
    else:
        try:
            tg.mandar_texto(args[0], " ".join(args[1:]))
        except Exception as e:
            tg.mandar_texto(msg["chat_id"], "Id de canal inválido", msg["msg_id"])

def c_decir_debug(args, msg):
    print("id (ignorado): " + args[0])
    print(" ".join(args[1:]))

async def c_sticker_discord(args, msg):
    await msg.channel.send("Aún no implementado")

def c_sticker_telegram(args, msg):
    if (len(args) < 2):
        tg.mandar_texto(msg["chat_id"], "Faltan argumentos", msg["msg_id"])
    else:
        try:
            tg.mandar_sticker(args[0], args[1])
        except Exception as e:
            tg.mandar_texto(msg["chat_id"], "Id de canal o de sticker inválido", msg["msg_id"])

def c_sticker_debug(args, msg):
    print("Mandar " + args[1] + " a " + args[0])

async def c_pic_discord(args, msg):
    await msg.channel.send("Aún no implementado")

def c_pic_telegram(args, msg):
    if (len(args) < 2):
        tg.mandar_texto(msg["chat_id"], "Faltan argumentos", msg["msg_id"])
    else:
        try:
            tg.mandar_imagen_por_id(args[0], args[1], " ".join(args[2:]))
        except Exception as e:
            tg.mandar_texto(msg["chat_id"], "Id de canal o de imagen inválido", msg["msg_id"])

def c_pic_debug(args, msg):
    print("Mandar " + args[1] + " a " + args[0])

async def c_gps_discord(args, msg):
    await msg.channel.send(buscar_gps(list(map(lambda x : limpiar(x), args))))

def c_gps_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], buscar_gps(list(map(lambda x : limpiar(x), args))), msg["msg_id"])

def c_gps_debug(args, msg):
    print(buscar_gps(list(map(lambda x : limpiar(x), args))))

def buscar_gps(args):
    if len(args) == 0:
        return "¿Qué estás buscando?"
    encontrados = {}
    for p in gps:
        en_este_pabellon = {}
        for f in gps[p]:
            en_este_piso = []
            for c in gps[p][f]:
                if c == '_':
                    en_este_piso = en_este_piso + agregar_lugares(gps[p][f][c], args, '')
                elif coincide_con(args[0], c):
                    en_este_piso = en_este_piso + agregar_lugares(gps[p][f][c], args[1:], c)
                else:
                    en_este_piso = en_este_piso + agregar_lugares(gps[p][f][c], args, c)
            if len(en_este_piso) > 0:
                en_este_pabellon[f] = en_este_piso
        if len(en_este_pabellon.keys()) > 0:
            encontrados[p] = en_este_pabellon
    if len(encontrados.keys()) == 0:
        return "No encontré ningún lugar parecido a " + ' '.join(args)
    res = "Encontré los siguientes lugares:"
    for p in encontrados:
        for f in encontrados[p]:
            res += "\nEn " + mostrar_piso(p, f) + ":"
            for l in encontrados[p][f]:
                res += "\n * " + l
    return res

def agregar_lugares(mas_lugares, args, c):
    res = []
    # print(mas_lugares)
    # print(args)
    # print(c)
    if len(args) == 0:
        res = mas_lugares
    else:
        args = ' '.join(args)
        for x in mas_lugares:
            if coincide_con(args, x):
                res.append(x)
    if len(c) > 0:
        return list(map(lambda x : c + ' ' + x, res))
    return res

def coincide_con(texto, patron):
    patron = limpiar(patron)
    if texto == patron:
        return True
    if texto.isnumeric() and patron.isnumeric():
        return int(texto) == int(patron)
    if texto.isnumeric() and texto == patron[1:]:
        return True
    if texto == 'labo' and patron == 'laboratorio':
        return True
    patron_split = patron.split(' ')
    if len(patron_split) > 1:
        for p in patron_split:
            if texto == p:
                return True
    return False

def mostrar_piso(p, f):
    return {'ss':'el subsuelo','es':'el entresubsuelo','ep':'el entre piso','pb':'la planta baja',
        '1':'el primer piso','2':'el segundo piso','3':'el tercer piso','4':'el cuarto piso'}.get(
          f, "el piso " + f) + " del pabellón " + {"0":"Cero + infinito"}.get(p, p)

def limpiar(txt):
    return txt.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u').replace('(','').replace(')','')

async def c_plano_discord(args, msg):
    await msg.channel.send(buscar_plano(list(map(lambda x : x.lower(), args))))

def c_plano_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], buscar_plano(list(map(lambda x : x.lower(), args))), msg["msg_id"])

def c_plano_debug(args, msg):
    print(buscar_plano(list(map(lambda x : x.lower(), args))))

def listar(elementos):
    if len(elementos) == 1:
        return elementos[0]
    return ', '.join(elementos[:-1]) + ' y ' + elementos[-1]

def buscar_plano(args):
    lista_pabellones = list(urlPlanos.keys())
    if len(args) == 0:
        return "¿De qué pabellón? Tengo planos de los siguientes pabellones: " + listar(lista_pabellones)
    if args[0] in urlPlanos:
        lista_pisos = list(urlPlanos[args[0]].keys())
        if len(args) == 1:
            return "¿De qué piso? Tengo planos de los siguientes pisos del pabellón " + args[0] + ": " + listar(lista_pisos)
        if args[1] in urlPlanos[args[0]]:
            return urlPlanos[args[0]][args[1]]
        return "No tengo esos planos. Tengo planos de los siguientes pisos del pabellón " + args[0] + ": " + listar(lista_pisos)
    return "No tengo esos planos. Tengo planos de los siguientes pabellones: " + listar(lista_pabellones)

async def c_menu_discord(args, msg):
    respuesta = menu(args)
    if not (respuesta is None):
        await msg.channel.send(respuesta)

def c_menu_telegram(args, msg):
    respuesta = menu(args)
    if not (respuesta is None):
        tg.mandar_texto(msg["chat_id"], respuesta, msg["msg_id"])

def c_menu_debug(args, msg):
    print(menu(args))

def menu(args):
    info = {}
    if len(args) > 0:
        arg = args[0]
        fecha = arg.split("/")
        if len(fecha) == 2:
            try:
                dia = int(fecha[0])
                mes = int(fecha[1])
                hoy = dia_de_hoy()
                fecha = nueva_fecha(hoy.year, mes, dia)
                if fecha < hoy:
                    fecha = fecha.replace(year = fecha.year + 1)
                info["fecha"] = fecha
            except Exception as e:
                print(e)
    return menu_comedor(info)

async def c_ralondario_discord(args, msg):
    respuesta = ralondario(args)
    if not (respuesta is None):
        await msg.channel.send(respuesta)

def c_ralondario_telegram(args, msg):
    respuesta = ralondario(args)
    if not (respuesta is None):
        tg.mandar_texto(msg["chat_id"], respuesta, msg["msg_id"])

def c_ralondario_debug(args, msg):
    print(ralondario(args))

def ralondario(args):
    info = {}
    if len(args) > 0:
        arg = args[0]
        try:
            n = int(arg)
            info["cantidad"] = n
            if n < 1:
                return None
            info["recortar_en"] = "cantidad"
        except:
            fecha = arg.split("/")
            if len(fecha) == 2:
                try:
                    dia = int(fecha[0])
                    mes = int(fecha[1])
                    hoy = dia_de_hoy()
                    fecha = nueva_fecha(hoy.year, mes, dia)
                    if fecha < hoy:
                        fecha = fecha.replace(year = fecha.year + 1)
                    info["dias"] = (fecha - hoy).days
                    info["recortar_en"] = "dias"
                except:
                    pass
    return proximos_eventos_ralondario(info)

async def c_gracias_discord(args, msg):
    await msg.channel.send("De nada")

def c_gracias_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], "De nada", msg["msg_id"])

def c_gracias_debug(args, msg):
    print("De nada")

async def c_dalu_discord(args, msg):
    await msg.channel.send("dalu@de.fcen.uba.ar")

def c_dalu_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], "dalu@de.fcen.uba.ar", msg["msg_id"])

def c_dalu_debug(args, msg):
    print("dalu@de.fcen.uba.ar")

async def c_test_discord(args, msg):
    await msg.channel.send("DEBUG")
    await msg.channel.send(file=discord.File(imagen_proxima_tesis(["Pepe grillo", "10:45"])))

def c_test_telegram(args, msg):
    tg.mandar_texto(msg["chat_id"], "DEBUG", msg["msg_id"])
    tg.mandar_archivo(msg["chat_id"], imagen_proxima_tesis(["Pepe grillo", "10:45"]))

def c_test_debug(args, msg):
    print("DEBUG")

comandos_validos = {
    "man":{
        "f_discord":c_man_discord,
        "f_telegram":c_man_telegram,
        "f_debug":c_man_debug,
        "ayuda":[
            "Ver lista de comandos",
            "Responde con la lista de comandos y una breve descripción de cada uno. " +
            "Si se le pasa como argumento el nombre de un comando en lugar de listarlos todos devuelve los detalles de dicho comando. " +
            "Ejemplos: \"man\" para la lista de comandos ; \"man man\" para los detalles del comando man."
        ]
    },
    "porque":{
        "f_discord":c_porque_discord,
        "f_telegram":c_porque_telegram,
        "f_debug":c_porque_debug,
        "ayuda":[
            "Preguntar por qué algo está hecho de esa forma",
            "Responde con el origen de alguna de esas cosas que en 10 años van a preguntar wtf por qué esto está hecho así.",
            "Se le debe pasar como argumento aquello de lo cual se quiere conocer su origen."
        ]
    },
    "flan":{
        "f_discord":c_flan_discord,
        "f_telegram":c_flan_telegram,
        "f_debug":c_flan_debug,
        "ayuda":[
            "Ver el plan de estudios",
            "Responde con la imagen del grafo con el plan de estudios.",
            "Se le puede pasar 'n' para el nuevo, 'v' para el viejo o 'd' para el de LCD."
        ]
    },
    "plan":{
        "hidden":True,
        "f_discord":c_flan_discord,
        "f_telegram":c_flan_telegram,
        "f_debug":c_flan_debug,
        "ayuda":[
            "Ver el plan de estudios",
            "Responde con la imagen del grafo con el plan de estudios.",
            "Se le puede pasar 'n' para el nuevo, 'v' para el viejo o 'd' para el de LCD."
        ]
    },
    "horarios":{
        "f_discord":c_horarios_discord,
        "f_telegram":c_horarios_telegram,
        "f_debug":c_horarios_debug,
        "ayuda":[
            "Ver los horarios de las materias",
            "Responde con el link a la planilla con los horarios de cada materia"
        ]
    },
    "menu":{
        "f_discord":c_menu_discord,
        "f_telegram":c_menu_telegram,
        "f_debug":c_menu_debug,
        "ayuda":[
            "Ver el menú del comedor",
            "Responde con el menú universitario del comedor de la facultad.",
            "Se le puede como parámetro una fecha en formato dd/mm para obtener el menú de un día particular.",
            "Si no se le pasa ningún parámetro devuelve el menú del día actual."
        ]
    },
    "tasks":{
        "f_discord":c_recordatorios_discord,
        "f_telegram":c_recordatorios_telegram,
        "f_debug":c_recordatorios_debug,
        "ayuda":[
            "Listar tareas periódicas",
            "Responde con la lista de tareas agendadas. " +
            "Si se le pasa como argumento el nombre de una tarea en lugar de listarlas todas devuelve los detalles de dicha tarea. " +
            "Ejemplos: \"tasks\" para la lista de tareas ; \"task ABRIR_LA_NORIEGA\" para los detalles de la tarea que abre la Noriega."
        ]
    },
    "say":{
        "hidden":True,
        "f_discord":c_decir_discord,
        "f_telegram":c_decir_telegram,
        "f_debug":c_decir_debug,
        "ayuda":[
            "Enviar un mensaje personalizado",
            "Envía un mensaje de texto a un grupo o canal. " +
            "Se le debe pasar como argumento un id de grupo o de canal y un mensaje de al menos una palabra. " +
            "Ejemplos: \"say 0042 Buenos días\" para mandar \"Buenos días\" al grupo o canal con id 0042 (debe ser un id válido en el que tenga permisos para mandar mensajes)."
        ]
    },
    "sticker":{
        "hidden":True,
        "f_discord":c_sticker_discord,
        "f_telegram":c_sticker_telegram,
        "f_debug":c_sticker_debug,
        "ayuda":[
            "Enviar un sticker",
            "Envía un sticker a un grupo o canal. " +
            "Se le debe pasar como argumento un id de grupo o de canal y un id de sticker. " +
            "Ejemplos: \"sticker 0042 2400\" para mandar el sticker de id 2400 al grupo o canal con id 0042 (debe ser un id válido en el que tenga permisos para mandar mensajes)."
        ]
    },
    "pic":{
        "hidden":True,
        "f_discord":c_pic_discord,
        "f_telegram":c_pic_telegram,
        "f_debug":c_pic_debug,
        "ayuda":[
            "Enviar una imagen",
            "Envía una imagen a un grupo o canal. " +
            "Se le debe pasar como argumento un id de grupo o de canal y un id de imagen. También se le puede pasar un mensaje como epígrafe. " +
            "Ejemplos: \"pic 0042 2400\" para mandar la imagen de id 2400 al grupo o canal con id 0042 sin epígrafe ; \"pic 0042 2400 Hola, ¿cómo te va?\" para mandar la imagen de id 2400 al grupo o canal con id 0042 con el epígrafe \"Hola, ¿cómo te va?\" (debe ser un id válido en el que tenga permisos para mandar mensajes)."
        ]
    },
    "plano":{
        "f_discord":c_plano_discord,
        "f_telegram":c_plano_telegram,
        "f_debug":c_plano_debug,
        "ayuda":[
            "Ver el plano de un piso de un edificio",
            "Responde con el plano de un piso de uno de los edificios de Exactas.",
            "Se le debe pasar como argumento un número de pabellón (0, 1 o 2) y un número de piso (0, o 1).",
            "Ejemplos: \"plano 0 0\" para los planos de la planta baja del cero más infinito."
        ]
    },
    "gps":{
        "f_discord":c_gps_discord,
        "f_telegram":c_gps_telegram,
        "f_debug":c_gps_debug,
        "ayuda":[
            "Ubicar un aula, laboratorio u otro lugar de la facultad",
            "Responde con una lista de lugares y sus ubicaciones.",
            "Se le debe pasar como argumento el nombre del lugar que se quiere ubicar (o parte del mismo).",
            "Ejemplos: \"gps aula 10\" para buscar todas las aulas con número 10 ; \"gps biblioteca\" para buscar todas las bibliotecas."
        ]
    },
    "cal":{
        "f_discord":c_ralondario_discord,
        "f_telegram":c_ralondario_telegram,
        "f_debug":c_ralondario_debug,
        "ayuda":[
            "Mostrar calendario académico",
            "Responde con una lista de próximos eventos en el calendario académico. " +
            "Si se le pasa como argumento un número devuelve esa cantidad de eventos. " +
            "Si se le pasa como argumento una fecha (dos números separados por una diagonal) devuelve todos los eventos hasta esa fecha inclusive. " +
            "Si no se le pasa ningún argumento muestra hasta 10 eventos dentro de los próximos 7 días. " +
            "Ejemplos: \"cal\" para ver hasta 10 eventos de la próxima semana ; \"cal 5\" para ver los próximos 5 eventos ; \"cal 10/5\" para ver los eventos hasta el 10 de mayo."
        ]
    },
    "gracias":{
        "f_discord":c_gracias_discord,
        "f_telegram":c_gracias_telegram,
        "f_debug":c_gracias_debug,
        "ayuda":[
            "Agradecer",
            "Responde al agradecimiento."
        ]
    },
    "dalu":{
        "f_discord":c_dalu_discord,
        "f_telegram":c_dalu_telegram,
        "f_debug":c_dalu_debug,
        "ayuda":[
            "Mail de Dalu",
            "Responde con el mail de la Dirección de Estudiantes."
        ]
    },
    "test":{
        "hidden":True,
        "f_discord":c_test_discord,
        "f_telegram":c_test_telegram,
        "f_debug":c_test_debug,
        "ayuda":[
            "Test",
            "Para debuggear."
        ]
    }
}

def imagen_proxima_tesis(tesis):
    return "files/heman.jpg"
    # tesista = tesis[0]
    # hora_tesis = tesis[1]
    # outfile = "tmp/"+tesista.replace(" ","_")+".png"
    # imagen = imageDraw.abrir_imagen("files/heman.jpg")
    # imagen.escribir(tesista, [120,120], tamaño=30, color=[255,255,255])
    # imagen.escribir(hora_tesis, [450,170], tamaño=40, color=[255,255,255])
    # imagen.guardar_imagen(outfile)
    # return outfile
