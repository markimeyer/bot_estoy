#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import tweepy
import random
import pymysql
import datetime

# Importar configuraciones de Twitter y MySQL
from config import consumer_key, consumer_secret, access_token, access_token_secret, host, user, password, database

# Conexión a Twitter APPS
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Conexión a BD MySQL
connection = pymysql.connect(host, user, password, database)

# Almacenamos la fecha de hoy
now = datetime.datetime.now().date()

# Cálculo de cuantos segundos tiene un día
segundos_dia = 60*60*24-1

# Randomizamos el segundo del día en el que se va a tuitear
retraso = random.randint(0, segundos_dia)

# Creamos el string de la hora según
m, s = divmod(retraso, 60)
h, m = divmod(m, 60)
hora = "%d:%02d:%02d" % (h, m, s)

# print(retraso)
# print(hora)

# Configuración de cursor para Base de Datos
try:
    with connection.cursor() as cursor:

        sql = "INSERT INTO `tweets` (`tweet`, `fecha`, `hora`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (0, now, hora))

    connection.commit()

#    with connection.cursor() as cursor:
#        # Read a single record
#        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#        cursor.execute(sql, ('webmaster@python.org',))
#        result = cursor.fetchone()
#        print(result)
finally:
    connection.close()

# Función para Tuitear "Estoy"
def tuitear():
	api.update_status(status="Estoy")

# Tiempo de espera para tuitear
t = threading.Timer(retraso, tuitear)

# Tuitear
t.start()
