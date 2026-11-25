# Guion de la exposición (unos 5 minutos)

## Ensayo

1. Haga un ensayo completo siguiendo este guion y mida el tiempo.
2. Al terminar, deje la base limpia para que el usuario nuevo vuelva a tener el id 4:

   ```powershell
   cmd /c "C:\xampp\mysql\bin\mysql.exe -u root -t --default-character-set=utf8mb4 < database.sql"
   ```

## Antes de la exposición (10 minutos antes)

1. **XAMPP Control Panel:** **Start** en **MySQL** y en **Apache** (los dos en verde).
2. **Base limpia:** ejecute el comando de arriba. Deben aparecer Laura, Andrés y Marta.
3. **Servidor** (en su propia ventana, desde `C:\xampp\htdocs\mini-crud`):

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
   ```

4. Deje abiertos:
   - **Postman** con la colección *Mini CRUD de usuarios*.
   - **phpMyAdmin** en <http://localhost/phpMyAdmin/>, en la tabla `mini_crud` → `usuarios`.
   - **VS Code** con `main.py` abierto.
   - **Navegador** en <http://localhost:8000/docs> (plan B).

## Guion

### 1. Presentación (30 s)

> "Hicimos una API que permite crear, ver, editar y borrar usuarios guardados en MySQL.
> Eso se llama CRUD: Create, Read, Update y Delete. Está hecha en Python con FastAPI."

### 2. El código (1 min), en VS Code

- **`database.sql`**: "La tabla `usuarios` tiene id automático, nombre, correo único y fecha de creación."
- **`.env` y `conexion.py`**: "La contraseña no está en el código: está en `.env`, que no se sube a GitHub.
  Además usamos un usuario de MySQL que solo tiene permisos sobre esta base."
- **`main.py`**: "Aquí están los 6 endpoints. `UsuarioEntrada` define qué datos son obligatorios.
  En el SQL usamos `%s` para que nadie pueda hacer inyección SQL."

### 3. Demostración en Postman (2 min 30 s)

| # | Petición | Qué decir | Mostrar en phpMyAdmin |
|---|---|---|---|
| 1 | Salud | "El servidor está encendido: 200 OK." | |
| 2 | Listar | "Estos son los 3 usuarios de ejemplo." | |
| 3 | Crear | Abrir **Body**. "Enviamos nombre y correo; responde 201 Created y el nuevo id." | ✅ Actualizar: aparece Carlos |
| 4 | Ver uno | "Pedimos solo ese usuario por su id." | |
| 5 | Editar | Abrir **Body**. "Cambiamos el nombre: 200 OK." | ✅ Actualizar: el nombre cambió |
| 6 | Correo repetido | "El correo de Laura ya existe: 409 Conflict. Lo impide la regla UNIQUE de la base." | |
| 7 | Sin nombre | "Falta el nombre: 422. FastAPI lo rechaza antes de llegar a la base." | |
| 8 | Borrar | "Borramos el usuario: 204 No Content." | ✅ Actualizar: Carlos ya no está |
| 9 | Ver borrado | "Ya no existe: 404 Not Found." | |

En cada petición, señale abajo el **código** y la pestaña **Test Results** en verde.

### 4. Cierre (1 min)

- Ejecute la colección completa: **...** → **Run** → **Start run**. Muestre **Passed 16, Failed 0**.
- "También tenemos 9 pruebas automáticas con pytest", y si da tiempo:

  ```powershell
  .\.venv\Scripts\python.exe -m pytest -v
  ```

- "Gracias. ¿Preguntas?"

## Plan B

| Si pasa esto | Haga esto |
|---|---|
| Postman no abre o falla | Use <http://localhost:8000/docs>: en cada endpoint, **Try it out** → **Execute** |
| Error de conexión a la base (500) | Revise que MySQL esté en verde en XAMPP |
| `Could not connect` en Postman | El servidor no está encendido: repita el paso 3 de "Antes de la exposición" |
| La petición 4 da 404 o la URL termina en `/usuarios/` | Envíe primero la petición 3 (guarda el id) |
| El nuevo usuario no tiene id 4 | No importa; explíquelo: "el contador de MySQL no retrocede al borrar" |
| MySQL no arranca en XAMPP | Revise `C:\xampp\mysql\data\mysql_error.log` |

## Preguntas probables del profesor

**¿Qué es una API?**
Un programa que recibe peticiones y responde con datos. No tiene pantalla: la usan otros programas, como Postman o una página web.

**¿Por qué FastAPI?**
Es sencillo, valida los datos solo con Pydantic y crea la página `/docs` automáticamente.

**¿Qué diferencia hay entre 404, 409 y 422?**
404: lo que pide no existe. 409: choca con una regla (correo repetido). 422: los datos enviados están mal o incompletos.

**¿Por qué no usan root?**
Por seguridad: el usuario `mini_crud` solo puede tocar su base. Si alguien roba la contraseña, no puede dañar otras bases.

**¿Dónde está la contraseña?**
En `.env`, que está en `.gitignore` y no se sube a GitHub. En GitHub solo está `.env.example`, sin la contraseña real.

**¿Qué es la inyección SQL y cómo la evitan?**
Es meter código SQL en un dato para alterar la consulta. La evitamos con `%s`: PyMySQL pone cada valor de forma segura, nunca pegado dentro del SQL.

**¿Por qué el correo se guarda en minúsculas?**
Para que `Laura@Ejemplo.test` y `laura@ejemplo.test` cuenten como el mismo correo.

**¿Qué pasa si borro y vuelvo a crear?**
El nuevo usuario recibe un id mayor: MySQL no reutiliza los números.

**¿Para qué sirven las pruebas automáticas?**
Para comprobar en segundos que todo sigue funcionando después de cambiar el código, sin hacerlo a mano.
