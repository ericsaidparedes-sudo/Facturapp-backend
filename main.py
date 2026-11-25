"""
Archivo:  mini-crud/main.py
Proyecto: Mini CRUD de usuarios

Qué hace:
    Es el servidor. Crea la API con FastAPI y define 6 endpoints:

        GET    /salud            comprobar que el servidor está encendido
        GET    /usuarios         listar todos los usuarios
        GET    /usuarios/{id}    ver un usuario
        POST   /usuarios         crear un usuario
        PUT    /usuarios/{id}    editar un usuario
        DELETE /usuarios/{id}    borrar un usuario

Cómo se ejecuta (desde la carpeta mini-crud, con el entorno virtual):
    .venv\\Scripts\\python.exe -m uvicorn main:app --reload --port 8000

    Después:
        http://localhost:8000/salud   responde {"estado": "ok"}
        http://localhost:8000/docs    página para probar la API desde el navegador

Conceptos:
    - Endpoint: una dirección + un método HTTP (GET, POST, PUT, DELETE).
    - CRUD: Create (crear, POST), Read (leer, GET), Update (editar, PUT),
      Delete (borrar, DELETE).
    - Pydantic (BaseModel): define la forma de los datos. Si llega un dato
      que no cumple (por ejemplo, sin nombre), FastAPI responde 422 solo.
    - HTTPException: detiene el endpoint y responde con un código de error
      (404 no existe, 409 conflicto) y un mensaje.
    - %s en el SQL: el lugar donde PyMySQL pone cada valor de forma
      segura. NUNCA se pega el texto del usuario dentro del SQL, porque
      eso permitiría "inyección SQL".
"""

from datetime import datetime

import pymysql
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

from conexion import obtener_conexion

# La aplicación. El título aparece en la página /docs.
app = FastAPI(title="Mini CRUD de usuarios",
              description="Demostración: crear, listar, ver, editar y borrar usuarios en MySQL.")


# ---------------------------------------------------------------- forma de los datos

class UsuarioEntrada(BaseModel):
    """Los datos que se envían para crear o editar un usuario."""
    # Obligatorio, de 1 a 100 caracteres.
    nombre: str = Field(min_length=1, max_length=100, examples=["Carlos Pérez"])
    # Obligatorio, con forma de correo: algo@algo.algo
    correo: str = Field(max_length=150, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                        examples=["carlos.perez@ejemplo.test"])


class Usuario(BaseModel):
    """Un usuario tal como lo devuelve la API."""
    id: int
    nombre: str
    correo: str
    creado_en: datetime


# Mensaje que se repite en varios endpoints.
NO_EXISTE = "El usuario no existe."
CORREO_REPETIDO = "Ya existe un usuario con ese correo."


# ---------------------------------------------------------------- endpoints

@app.get("/salud")
def salud() -> dict:
    """Responde que el servidor está encendido. No usa la base de datos."""
    return {"estado": "ok"}


@app.get("/usuarios", response_model=list[Usuario])
def listar_usuarios():
    """READ: devuelve todos los usuarios, del más antiguo al más nuevo."""
    with obtener_conexion() as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, correo, creado_en FROM usuarios ORDER BY id")
        return cursor.fetchall()


@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def ver_usuario(usuario_id: int):
    """READ: devuelve un usuario por su id, o 404 si no existe."""
    with obtener_conexion() as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, correo, creado_en FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
    if usuario is None:
        raise HTTPException(status_code=404, detail=NO_EXISTE)
    return usuario


@app.post("/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioEntrada):
    """CREATE: crea un usuario y lo devuelve con su id. 409 si el correo ya existe."""
    with obtener_conexion() as conexion, conexion.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)",
                           (datos.nombre.strip(), datos.correo.strip().lower()))
        except pymysql.err.IntegrityError:
            # La base de datos rechaza el correo repetido (restricción UNIQUE).
            raise HTTPException(status_code=409, detail=CORREO_REPETIDO)
        nuevo_id = cursor.lastrowid  # el id que MySQL le asignó
        cursor.execute("SELECT id, nombre, correo, creado_en FROM usuarios WHERE id = %s", (nuevo_id,))
        return cursor.fetchone()


@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def editar_usuario(usuario_id: int, datos: UsuarioEntrada):
    """UPDATE: cambia el nombre y el correo. 404 si no existe, 409 si el correo es de otro usuario."""
    with obtener_conexion() as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail=NO_EXISTE)
        try:
            cursor.execute("UPDATE usuarios SET nombre = %s, correo = %s WHERE id = %s",
                           (datos.nombre.strip(), datos.correo.strip().lower(), usuario_id))
        except pymysql.err.IntegrityError:
            raise HTTPException(status_code=409, detail=CORREO_REPETIDO)
        cursor.execute("SELECT id, nombre, correo, creado_en FROM usuarios WHERE id = %s", (usuario_id,))
        return cursor.fetchone()


@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_usuario(usuario_id: int):
    """DELETE: borra el usuario de verdad. Responde 204 (sin contenido) o 404 si no existe."""
    with obtener_conexion() as conexion, conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        if cursor.rowcount == 0:  # rowcount: cuántas filas se borraron
            raise HTTPException(status_code=404, detail=NO_EXISTE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
