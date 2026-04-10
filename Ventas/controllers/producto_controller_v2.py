from config.database import conectar
from utils.validaciones import validar_nombre, validar_precio
import re
import sqlite3


def _validar_color_hex(color):
    return re.match(r"^#[0-9A-Fa-f]{6}$", color.strip()) is not None


def _normalizar_datos_producto(nombre, precio, color, leyenda):
    nombre = nombre.strip()
    color = color.strip().upper()
    leyenda = leyenda.strip()

    if nombre == "":
        return False, "El nombre no puede estar vacio.", None

    if not validar_nombre(nombre):
        return False, "El nombre contiene caracteres no permitidos.", None

    if not validar_precio(precio):
        return False, "El precio debe ser numerico y mayor que 0.", None

    if not _validar_color_hex(color):
        return False, "El color debe tener formato HEX, por ejemplo #FFAA00.", None

    if len(leyenda) > 120:
        return False, "La leyenda no puede superar 120 caracteres.", None

    return True, "", (nombre, float(precio), color, leyenda)


def agregar_producto(nombre, precio, color="#FFFFFF", leyenda=""):
    valido, mensaje, datos = _normalizar_datos_producto(nombre, precio, color, leyenda)
    if not valido:
        return False, mensaje

    nombre, precio, color, leyenda = datos

    with conectar() as conexion:
        conexion.execute(
            "INSERT INTO productos (nombre, precio, color, leyenda) VALUES (?, ?, ?, ?)",
            (nombre, precio, color, leyenda),
        )

    return True, "Producto agregado correctamente."


def listar_productos():
    with conectar() as conexion:
        cursor = conexion.execute(
            "SELECT id_producto, nombre, precio, color, leyenda FROM productos"
        )
        return cursor.fetchall()


def buscar_producto_por_id(id_producto):
    with conectar() as conexion:
        cursor = conexion.execute(
            "SELECT id_producto, nombre, precio, color, leyenda FROM productos WHERE id_producto = ?",
            (id_producto,),
        )
        return cursor.fetchone()


def actualizar_producto(id_producto, nuevo_nombre, nuevo_precio, nuevo_color="#FFFFFF", nueva_leyenda=""):
    valido, mensaje, datos = _normalizar_datos_producto(
        nuevo_nombre, nuevo_precio, nuevo_color, nueva_leyenda
    )
    if not valido:
        return False, mensaje

    nuevo_nombre, nuevo_precio, nuevo_color, nueva_leyenda = datos

    with conectar() as conexion:
        cursor = conexion.execute(
            "SELECT id_producto FROM productos WHERE id_producto = ?",
            (id_producto,),
        )
        if cursor.fetchone() is None:
            return False, "No existe un producto con ese ID."

        conexion.execute(
            """
            UPDATE productos
            SET nombre = ?, precio = ?, color = ?, leyenda = ?
            WHERE id_producto = ?
            """,
            (nuevo_nombre, nuevo_precio, nuevo_color, nueva_leyenda, id_producto),
        )

    return True, "Producto actualizado correctamente."


def eliminar_producto(id_producto):
    with conectar() as conexion:
        cursor = conexion.execute(
            "SELECT id_producto FROM productos WHERE id_producto = ?",
            (id_producto,),
        )
        if cursor.fetchone() is None:
            return False, "No existe un producto con ese ID."

        try:
            conexion.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
        except sqlite3.IntegrityError:
            return False, "No se puede eliminar el producto porque esta usado en ventas registradas"

    return True, "Producto eliminado correctamente."
