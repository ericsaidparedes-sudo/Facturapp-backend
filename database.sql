-- Crea la base de datos si no existe. utf8mb4 guarda bien tildes y ñ.
CREATE DATABASE IF NOT EXISTS mini_crud
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE mini_crud;

-- Borra la tabla si ya existía, para poder ejecutar el archivo varias veces.
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id        INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre    VARCHAR(100) NOT NULL,
    correo    VARCHAR(150) NOT NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_usuarios PRIMARY KEY (id),
    CONSTRAINT uq_usuarios_correo UNIQUE (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos de ejemplo para la demostración.
INSERT INTO usuarios (nombre, correo) VALUES
    ('Laura Gómez',  'laura.gomez@ejemplo.test'),
    ('Andrés Muñoz', 'andres.munoz@ejemplo.test'),
    ('Marta Rincón', 'marta.rincon@ejemplo.test');

-- Comprobación: debe mostrar los 3 usuarios.
SELECT id, nombre, correo, creado_en FROM usuarios;
