#!/usr/bin/python3
# -*- coding: utf-8 -*-
from random import random, randint
import cv2

def abrir_imagen(ruta_imagen):
  return ImagenDibujable(ruta_imagen)

class ImagenDibujable:
  def __init__(self, ruta):
    self.img = cv2.imread(ruta, 1)
    self.defaults = {
      "font":cv2.FONT_HERSHEY_COMPLEX,
      "pointsize":20,
      "fill":(0, 0, 0)
    }

  # cv2.FONT_ ...
  def set_fuente(self, font):
    self.defaults["font"] = font

  # número
  def set_tamaño(self, size):
    self.defaults["pointsize"] = size

  # (número, número, número)
  def set_color(self, color):
    self.defaults["fill"] = color

  # texto : string
  # posicion : (número, número)
  # color : (número, número, número)
  # tamaño : número
  # fuente : cv2.FONT_ ...
  def escribir(self, texto, posicion, color=None, tamaño=None, fuente=None):
    if color is None:
      color = self.defaults["fill"]
    if tamaño is None:
      tamaño = self.defaults["pointsize"]
    if fuente is None:
      fuente = self.defaults["font"]
    cv2.putText(self.img,texto,posicion,fuente,tamaño/30.0,color,2)

  def guardar_imagen(self, ruta):
    try:
        cv2.imwrite(ruta, self.img)
    except:
        print("Error al guardar imagen")

def random_text(filein, text, imgsize, n, fileout):
  imagen = abrir_imagen(filein)
  w = imgsize[0]
  h = imgsize[1]
  for i in range(n):
    imagen.escribir(text,
      (randint(int(-w/120),int(2*w/3)),randint(int(h/6),int(5*h/6))),
      tamaño=randint(int(w/60),int(w/10)),
      color=(randint(50,250),randint(50,250),randint(50,250),0.4+random()/2))
  imagen.guardar_imagen(fileout)
