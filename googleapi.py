from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from fechayhora import dia_de_hoy, fecha_desde_str

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def cargar_calendario_google_api(ID, n, rango_dias, corte):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    if (ID is None):
        ID = 'primary'
    else:
        ID += '@group.calendar.google.com'

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=ID, timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    eventos = events_result.get('items', [])
    if corte == "ambos" or corte == "dias":
        hoy = dia_de_hoy()
        ultimo = obtener_ultimo_valido(eventos, hoy, rango_dias)
        if ultimo == len(eventos):
            if corte == "dias":
                eventos += pedir_mas_eventos(service, eventos[-1], ID, n, rango_dias, hoy)
        else:
            eventos = eventos[:ultimo]
    return eventos

def obtener_ultimo_valido(eventos, hoy, rango_dias):
    ultimo = 0
    for evento in eventos:
        inicio = fecha_evento(evento)
        if (inicio-hoy).days <= rango_dias:
            ultimo += 1
        else:
            return ultimo
    return ultimo

def fecha_evento(evento):
    inicio = evento['start']
    if ('date' in inicio):
        inicio = inicio['date']
    elif ('dateTime' in inicio):
        inicio = inicio['dateTime'][:10]
    else:
        inicio = '2100-01-01'
    return fecha_desde_str(inicio)

def pedir_mas_eventos(service, ultimo, ID, n, rango_dias, hoy):
    mas_eventos = []
    inicio = fecha_evento(ultimo)
    intentos = 10
    while((inicio-hoy).days <= rango_dias and intentos > 0):
        mas = service.events().list(calendarId=ID, timeMin=datetime.datetime.fromordinal(inicio.toordinal()).isoformat() + 'Z',
                                        maxResults=50, singleEvents=True,
                                        orderBy='startTime').execute()
        mas = mas.get('items', [])
        mas_eventos = agregar_sin_repetidos_(mas_eventos, mas)
        if len(mas) < n:
            break
        inicio = fecha_evento(mas_eventos[-1])
        intentos = intentos-1
    return mas_eventos[:obtener_ultimo_valido(mas_eventos, hoy, rango_dias)]

def agregar_sin_repetidos_(src, mas):
    for nuevo in mas:
        if not esta_repetido_en(nuevo, src):
            src.append(nuevo)
    return src

def esta_repetido_en(nuevo, eventos):
    for evento in eventos:
        if evento['start']['date'] == nuevo['start']['date'] and evento['summary'] == nuevo['summary']:
            return True
    return False

if __name__ == '__main__':
    eventos = cargar_calendario_google_api(None, 10)
    if not eventos:
        print('No upcoming events found.')
    for event in eventos:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
