"""
Archivo:  mini-crud/conexion.py
Proyecto: Mini CRUD de usuarios

Qué hace:
    Abre la conexión con la base de datos MySQL "mini_crud", leyendo los
    datos (servidor, usuario, contraseña...) del archivo .env.

Por qué los datos están en .env y no aquí:
    La contraseña nunca se escribe en el código. Así el código se puede
    subir a GitHub sin exponerla.

Conceptos:
    - load_dotenv(): lee el archivo .env y deja sus valores disponibles
      con os.getenv("NOMBRE").
    - DictCursor: cada fila llega como diccionario, por ejemplo
      {"id": 1, "nombre": "Laura Gómez"}, en lugar de (1, "Laura Gómez").
    - autocommit=True: cada cambio (INSERT, UPDATE, DELETE) se guarda en
      cuanto se ejecuta. En este proyecto cada endpoint hace un solo
      cambio, así que no hace falta manejar transacciones.
"""

import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv
from pymysql.cursors import DictCursor

# Carga el .env que está en la misma carpeta que este archivo.
load_dotenv(Path(__file__).parent / ".env")


def obtener_conexion() -> pymysql.connections.Connection:
    """Abre y devuelve una conexión nueva a la base de datos.

    Se usa con "with", que la cierra sola al terminar:
        with obtener_conexion() as conexion:
            ...
    """
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "mini_crud"),
        charset="utf8mb4",        # guarda bien las tildes y la ñ
        cursorclass=DictCursor,
        autocommit=True,
    )
