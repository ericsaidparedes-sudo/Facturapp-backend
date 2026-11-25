"""
Archivo:  mini-crud/test_usuarios.py
Proyecto: Mini CRUD de usuarios

Qué hace:
    Pruebas automáticas de los 6 endpoints. Hacen lo mismo que la colección
    de Postman, pero desde Python y con un solo comando.

Cómo se ejecuta (desde la carpeta mini-crud, con MySQL encendido):
    .venv\\Scripts\\python.exe -m pytest -v

    No hace falta encender el servidor: TestClient llama a la API
    directamente, sin usar el puerto 8000.

Cuidado con la base de datos:
    Las pruebas usan la base real "mini_crud". Cada prueba borra el usuario
    que crea, así que al final quedan los mismos usuarios que había. Lo único
    que cambia es el contador de id (el próximo id ya no será 4). Para
    dejarla como nueva, ejecute otra vez database.sql.

Conceptos:
    - pytest: busca las funciones que empiezan con "test_" y las ejecuta.
    - assert: comprueba que algo es verdad. Si no lo es, la prueba falla.
    - TestClient: un "Postman de mentiras" dentro de Python: envía
      peticiones a la API y devuelve la respuesta.
    - fixture: algo que pytest prepara antes de una prueba y limpia después.
"""

import time

import pytest
from fastapi.testclient import TestClient

from main import app

# El cliente que envía las peticiones a la API.
cliente = TestClient(app)


def correo_unico(prefijo: str) -> str:
    """Devuelve un correo que no se repite, usando la hora actual en nanosegundos."""
    return f"{prefijo}.{time.time_ns()}@ejemplo.test"


@pytest.fixture
def usuario_creado():
    """Crea un usuario de prueba antes de la prueba y lo borra después.

    "yield" entrega el usuario a la prueba. Cuando la prueba termina
    (salga bien o mal), se ejecuta lo que está después del yield.
    """
    respuesta = cliente.post("/usuarios", json={"nombre": "Usuario de Prueba",
                                                "correo": correo_unico("prueba")})
    usuario = respuesta.json()
    yield usuario
    cliente.delete(f"/usuarios/{usuario['id']}")  # limpieza (si ya se borró, responde 404 y no pasa nada)


# ---------------------------------------------------------------- pruebas

def test_salud():
    """GET /salud responde 200 y {"estado": "ok"}."""
    respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


def test_listar_usuarios():
    """GET /usuarios responde 200 y una lista."""
    respuesta = cliente.get("/usuarios")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def test_crear_usuario():
    """POST /usuarios responde 201, guarda el correo en minúsculas y devuelve el id."""
    correo = correo_unico("Nuevo.Usuario")  # con mayúsculas a propósito
    respuesta = cliente.post("/usuarios", json={"nombre": "Nuevo Usuario", "correo": correo})
    assert respuesta.status_code == 201
    usuario = respuesta.json()
    assert usuario["nombre"] == "Nuevo Usuario"
    assert usuario["correo"] == correo.lower()
    cliente.delete(f"/usuarios/{usuario['id']}")  # limpieza


def test_ver_usuario(usuario_creado):
    """GET /usuarios/{id} responde 200 con el usuario pedido."""
    respuesta = cliente.get(f"/usuarios/{usuario_creado['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == usuario_creado["id"]


def test_editar_usuario(usuario_creado):
    """PUT /usuarios/{id} responde 200 y cambia el nombre."""
    respuesta = cliente.put(f"/usuarios/{usuario_creado['id']}",
                            json={"nombre": "Nombre Editado", "correo": correo_unico("editado")})
    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Nombre Editado"


def test_crear_con_correo_repetido_da_409(usuario_creado):
    """POST /usuarios con un correo que ya existe responde 409."""
    respuesta = cliente.post("/usuarios", json={"nombre": "Otro", "correo": usuario_creado["correo"]})
    assert respuesta.status_code == 409
    assert respuesta.json()["detail"] == "Ya existe un usuario con ese correo."


def test_crear_sin_nombre_da_422():
    """POST /usuarios sin nombre responde 422 (FastAPI lo rechaza antes de llegar a la base)."""
    respuesta = cliente.post("/usuarios", json={"correo": correo_unico("sin.nombre")})
    assert respuesta.status_code == 422


def test_borrar_usuario(usuario_creado):
    """DELETE /usuarios/{id} responde 204 y después el usuario ya no existe (404)."""
    respuesta = cliente.delete(f"/usuarios/{usuario_creado['id']}")
    assert respuesta.status_code == 204
    respuesta = cliente.get(f"/usuarios/{usuario_creado['id']}")
    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "El usuario no existe."


def test_editar_usuario_que_no_existe_da_404():
    """PUT /usuarios/{id} con un id que no existe responde 404."""
    respuesta = cliente.put("/usuarios/999999", json={"nombre": "Nadie", "correo": correo_unico("nadie")})
    assert respuesta.status_code == 404
