from config.database import conectar
from utils.validaciones import validar_nombre, validar_precio

def agregar_producto(nombre, precio):
    nombre = nombre.strip()

    if nombre == "":
        return False, "El nombre no puede estar vacío."

    if not validar_nombre(nombre):
        return False, "El nombre contiene caracteres no permitidos."

    if not validar_precio(precio):
        return False, "El precio debe ser numérico y mayor que 0."

    precio = float(precio)

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
        (nombre, precio)
    )

    conexion.commit()
    conexion.close()

    return True, "Producto agregado correctamente."


def listar_productos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_producto, nombre, precio FROM productos")
    productos = cursor.fetchall()

    conexion.close()
    return productos


def buscar_producto_por_id(id_producto):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_producto, nombre, precio FROM productos WHERE id_producto = ?",
        (id_producto,)
    )
    producto = cursor.fetchone()

    conexion.close()
    return producto


def actualizar_producto(id_producto, nuevo_nombre, nuevo_precio):
    nuevo_nombre = nuevo_nombre.strip()

    if nuevo_nombre == "":
        return False, "El nombre no puede estar vacío."

    if not validar_nombre(nuevo_nombre):
        return False, "El nombre contiene caracteres no permitidos."

    if not validar_precio(nuevo_precio):
        return False, "El precio debe ser numérico y mayor que 0."

    nuevo_precio = float(nuevo_precio)

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_producto FROM productos WHERE id_producto = ?",
        (id_producto,)
    )
    producto = cursor.fetchone()

    if producto is None:
        conexion.close()
        return False, "No existe un producto con ese ID."

    cursor.execute(
        "UPDATE productos SET nombre = ?, precio = ? WHERE id_producto = ?",
        (nuevo_nombre, nuevo_precio, id_producto)
    )

    conexion.commit()
    conexion.close()

    return True, "Producto actualizado correctamente."


def eliminar_producto(id_producto):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_producto FROM productos WHERE id_producto = ?",
        (id_producto,)
    )
    producto = cursor.fetchone()

    if producto is None:
        conexion.close()
        return False, "No existe un producto con ese ID."

    cursor.execute(
        "DELETE FROM productos WHERE id_producto = ?",
        (id_producto,)
    )

    conexion.commit()
    conexion.close()

    return True, "Producto eliminado correctamente."