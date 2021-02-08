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
def cargar_calendario_icalevents(i, cantidad, rango_dias, corte, retries):
    # TODO: Considerar el argumento "corte"
    url = __calendar_url(i)
    now = aware_now()
    span = timedelta(days=rango_dias)
    start = (now - span)
    end = (now + span)
    while retries > 0:
        try:
            calendar_raw = icaldownload.ICalDownload().data_from_url(url)
            eventos = icalparser.parse_events(calendar_raw, start = start, end = end)
            eventos = filter((lambda x: es_posterior(x.start, now) and es_posterior(now + span, x.start)), eventos)
            eventos = sorted(eventos, key = (lambda x: x.start.date()))
            return eventos[:cantidad]
        except Exception:
            retries -= 1

    # Debería levantar una excepción?
    return []

def es_posterior(f1, f2):
  return f1.date() >= f2.date()

# Devuelve los n próximos eventos del calendario con un limite de l dias
def proximos_eventos(i, n, l, corte):
    # la comento porque icalevents tiene un bug al comparar fechas
    # return cargar_calendario_icalevents(i, n, l, corte, 3)

    # en su lugar, uso la api de Google
    return cargar_calendario_google_api(i, n, l, corte)
