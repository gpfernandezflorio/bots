#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from icalevents import icaldownload, icalparser
from datetime import datetime, timedelta
from pytz import timezone
from googleapi import cargar_calendario_google_api

# Devuelve el momento actual con nuestra zona horaria.
def aware_now():
    return datetime.now(tz=timezone('America/Buenos_Aires'))

# Genero la url del calendario a partir del id
def __calendar_url(i):
    return 'https://calendar.google.com/calendar/ical/' + str(i) + \
        '%40group.calendar.google.com/public/basic.ics'

# Cargo la data del calendario
def cargar_calendario_icalevents(i, retries, rango_dias=30):
    url = __calendar_url(i)
    now = aware_now()
    span = timedelta(days=rango_dias)
    start = (now - span)
    end = (now + span)
    while retries > 0:
        try:
            calendar_raw = icaldownload.ICalDownload().data_from_url(url)
            eventos = icalparser.parse_events(calendar_raw, start = start, end = end)
            return (eventos, now, span, calendar_raw)
        except Exception:
            retries -= 1

    # Debería levantar una excepción?
    return None

def es_posterior(f1, f2):
  return f1.date() >= f2.date()

# Devuelve los n próximos eventos del calendario con un limite de l dias
def proximos_eventos(i, n, l):
    # la comento porque icalevents tiene un bug al comparar fechas
    # proximos_eventos_icalevents(i, n, l)

    # en su lugar, uso la api de Google
    return proximos_eventos_google_api(i, n, l)

def proximos_eventos_icalevents(i, n, l):
    now = aware_now()
    span = timedelta(days=l)
    calendario = cargar_calendario_icalevents(i, 3, l)
    if calendario is None:
      return []
    eventos = calendario[0]
    eventos = filter((lambda x: es_posterior(x.start, now) and es_posterior(now + span, x.start)), eventos)
    eventos = sorted(eventos, key = (lambda x: x.start.date()))
    return eventos[:n]

def proximos_eventos_google_api(i, n, l):
    calendario = cargar_calendario_google_api(i, n)
    if calendario is None:
      return []
    eventos = calendario[0]
    return eventos
