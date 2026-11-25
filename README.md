# Mini CRUD de usuarios

API sencilla hecha con **FastAPI** y **MySQL** para crear, listar, ver, editar y borrar usuarios.
Es un proyecto de demostración: muestra los 4 tipos de operaciones (CRUD), los códigos de respuesta HTTP
y cómo probar una API con Postman y con pruebas automáticas.

## Qué tiene

| Archivo | Para qué sirve |
|---|---|
| `database.sql` | Crea la base `mini_crud`, la tabla `usuarios` y 3 usuarios de ejemplo |
| `.env.example` | Plantilla de los datos de conexión (sin la contraseña real) |
| `.env` | Datos de conexión reales. **No se sube a GitHub** |
| `requirements.txt` | Librerías de Python con su versión exacta |
| `conexion.py` | Abre la conexión con MySQL leyendo el `.env` |
| `main.py` | El servidor: la API con sus 6 endpoints |
| `test_usuarios.py` | 9 pruebas automáticas con pytest |
| `mini-crud.postman_collection.json` | Colección de Postman con 9 peticiones y 16 pruebas |
| `GUION.md` | Guion de la exposición |

## Endpoints

| Método | Ruta | Qué hace | Respuestas |
|---|---|---|---|
| GET | `/salud` | Comprobar que el servidor está encendido | 200 |
| GET | `/usuarios` | Listar todos | 200 |
| GET | `/usuarios/{id}` | Ver uno | 200, 404 |
| POST | `/usuarios` | Crear | 201, 409 (correo repetido), 422 (datos incompletos) |
| PUT | `/usuarios/{id}` | Editar | 200, 404, 409, 422 |
| DELETE | `/usuarios/{id}` | Borrar | 204, 404 |

## Requisitos

- Python 3.12
- MySQL o MariaDB (por ejemplo, el de XAMPP)
- Postman (opcional, para probar a mano)

## Instalación

Desde la carpeta del proyecto, en PowerShell:

```powershell
# 1. Crear la base de datos con los 3 usuarios de ejemplo
cmd /c "C:\xampp\mysql\bin\mysql.exe -u root -t --default-character-set=utf8mb4 < database.sql"

# 2. Crear el usuario de MySQL del proyecto (ver el tutorial, paso 1.5)

# 3. Copiar la plantilla y poner la contraseña real en .env
Copy-Item .env.example .env

# 4. Crear el entorno virtual e instalar las librerías
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Cómo arrancar

Con MySQL encendido:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

- <http://localhost:8000/salud> responde `{"estado":"ok"}`
- <http://localhost:8000/docs> es la página para probar la API desde el navegador

## Cómo probar

**Con Postman:** importe `mini-crud.postman_collection.json` (Ctrl + O) y ejecute la colección
(**Run** → **Start run**). Debe decir **Passed 16, Failed 0**.

**Con pytest** (no hace falta encender el servidor):

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Debe decir **9 passed**.

## Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/): el framework de la API
- [Uvicorn](https://uvicorn.dev/): el servidor
- [PyMySQL](https://github.com/PyMySQL/PyMySQL): la conexión con MySQL
- [python-dotenv](https://github.com/theskumar/python-dotenv): lee el `.env`
- [pytest](https://docs.pytest.org/): las pruebas automáticas
- MySQL / MariaDB: la base de datos
