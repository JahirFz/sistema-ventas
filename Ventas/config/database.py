import sqlite3
import os

RUTA_DB = os.path.join("database", "ventas.db")

def conectar():
    conn = sqlite3.connect(RUTA_DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def crear_tabla_clientes():
    with conectar() as conexion:

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        """)

def crear_tabla_productos():
    with conectar() as conexion:

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                color TEXT NOT NULL DEFAULT '#FFFFFF',
                leyenda TEXT NOT NULL DEFAULT ''
            )
        """)

        columnas = {
            fila[1] for fila in conexion.execute("PRAGMA table_info(productos)").fetchall()
        }
        if "color" not in columnas:
            conexion.execute(
                "ALTER TABLE productos ADD COLUMN color TEXT NOT NULL DEFAULT '#FFFFFF'"
            )
        if "leyenda" not in columnas:
            conexion.execute(
                "ALTER TABLE productos ADD COLUMN leyenda TEXT NOT NULL DEFAULT ''"
            )


def crear_tabla_ventas():
    with conectar() as conexion:

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                id_cliente INTEGER NOT NULL,
                requiere_factura INTEGER NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
            )
        """)
        conexion.execute(
            "CREATE INDEX IF NOT EXISTS idx_ventas_cliente ON ventas(id_cliente)"
        )


def crear_tabla_detalle_ventas():
    with conectar() as conexion:

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS detalle_ventas (
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                color TEXT NOT NULL DEFAULT '#FFFFFF',
                leyenda TEXT NOT NULL DEFAULT '',
                completado INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
                FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
            )
        """)

        columnas = {
            fila[1] for fila in conexion.execute("PRAGMA table_info(detalle_ventas)").fetchall()
        }
        if "color" not in columnas:
            conexion.execute(
                "ALTER TABLE detalle_ventas ADD COLUMN color TEXT NOT NULL DEFAULT '#FFFFFF'"
            )
        if "leyenda" not in columnas:
            conexion.execute(
                "ALTER TABLE detalle_ventas ADD COLUMN leyenda TEXT NOT NULL DEFAULT ''"
            )
        if "completado" not in columnas:
            conexion.execute(
                "ALTER TABLE detalle_ventas ADD COLUMN completado INTEGER NOT NULL DEFAULT 0"
            )
        conexion.execute(
            "CREATE INDEX IF NOT EXISTS idx_detalle_venta_id_venta ON detalle_ventas(id_venta)"
        )
        conexion.execute(
            "CREATE INDEX IF NOT EXISTS idx_detalle_venta_id_producto ON detalle_ventas(id_producto)"
        )
        conexion.execute(
            "CREATE INDEX IF NOT EXISTS idx_detalle_venta_completado ON detalle_ventas(completado)"
        )


def crear_tabla_pagos():
    with conectar() as conexion:

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS pagos (
                id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                monto REAL NOT NULL,
                metodo_pago TEXT NOT NULL,
                FOREIGN KEY (id_venta) REFERENCES ventas(id_venta)
            )
        """)
        conexion.execute(
            "CREATE INDEX IF NOT EXISTS idx_pagos_id_venta ON pagos(id_venta)"
        )
