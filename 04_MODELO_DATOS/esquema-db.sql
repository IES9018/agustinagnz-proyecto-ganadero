-- =========================================================
-- ESQUEMA BASE DE DATOS - GANADAPP
-- =========================================================

CREATE DATABASE ganadapp;

\c ganadapp;

-- =========================================================
-- TABLA: usuario
-- =========================================================

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    rol VARCHAR(50) NOT NULL,
    contacto VARCHAR(100),
    estado_activo BOOLEAN NOT NULL DEFAULT TRUE,
    ultimo_acceso TIMESTAMP
);

-- =========================================================
-- TABLA: productor
-- =========================================================

CREATE TABLE productor (
    id_productor SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    documento VARCHAR(50) NOT NULL UNIQUE,
    contacto VARCHAR(100),
    direccion VARCHAR(200),
    estado VARCHAR(50) NOT NULL
);

-- =========================================================
-- TABLA: establecimiento
-- =========================================================

CREATE TABLE establecimiento (
    id_establecimiento SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    ubicacion VARCHAR(200),
    capacidad INTEGER NOT NULL CHECK (capacidad >= 0),
    estado VARCHAR(50) NOT NULL,
    id_productor INTEGER NOT NULL,

    CONSTRAINT fk_establecimiento_productor
        FOREIGN KEY (id_productor)
        REFERENCES productor(id_productor)
);

-- =========================================================
-- TABLA: animal
-- =========================================================

CREATE TABLE animal (
    id_animal SERIAL PRIMARY KEY,
    identificador VARCHAR(100) NOT NULL UNIQUE,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(100),
    fecha_nacimiento DATE,
    estado_sanitario VARCHAR(100),
    id_establecimiento INTEGER NOT NULL,

    CONSTRAINT fk_animal_establecimiento
        FOREIGN KEY (id_establecimiento)
        REFERENCES establecimiento(id_establecimiento)
);

-- =========================================================
-- TABLA: evento_sanitario
-- =========================================================

CREATE TABLE evento_sanitario (
    id_evento SERIAL PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    fecha TIMESTAMP NOT NULL,
    descripcion TEXT,
    dosis VARCHAR(100),
    id_animal INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,

    CONSTRAINT fk_evento_animal
        FOREIGN KEY (id_animal)
        REFERENCES animal(id_animal),

    CONSTRAINT fk_evento_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
);

-- =========================================================
-- TABLA: stock_insumo
-- =========================================================

CREATE TABLE stock_insumo (
    id_stock SERIAL PRIMARY KEY,
    tipo_insumo VARCHAR(100) NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL DEFAULT 0,
    unidad VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(200),
    id_establecimiento INTEGER NOT NULL,

    CONSTRAINT chk_stock_no_negativo
        CHECK (cantidad >= 0),

    CONSTRAINT fk_stock_establecimiento
        FOREIGN KEY (id_establecimiento)
        REFERENCES establecimiento(id_establecimiento)
);