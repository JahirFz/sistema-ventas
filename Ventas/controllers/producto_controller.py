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

    with conectar() as conexion:

        conexion.execute(
            "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
            (nombre, precio)
        )

    return True, "Producto agregado correctamente."


def listar_productos():
    with conectar() as conexion:

        cursor = conexion.execute("SELECT id_producto, nombre, precio FROM productos")

        return cursor.fetchall()


def buscar_producto_por_id(id_producto):
    with conectar() as conexion:

        cursor = conexion.execute(
            "SELECT id_producto, nombre, precio FROM productos WHERE id_producto = ?",
            (id_producto,)
        )
    
        return cursor.fetchone()


def actualizar_producto(id_producto, nuevo_nombre, nuevo_precio):
    nuevo_nombre = nuevo_nombre.strip()

    if nuevo_nombre == "":
        return False, "El nombre no puede estar vacío."

    if not validar_nombre(nuevo_nombre):
        return False, "El nombre contiene caracteres no permitidos."

    if not validar_precio(nuevo_precio):
        return False, "El precio debe ser numérico y mayor que 0."

    nuevo_precio = float(nuevo_precio)

    with conectar() as conexion:

        cursor = conexion.execute(
            "SELECT id_producto FROM productos WHERE id_producto = ?",
            (id_producto,)
        )

        if  cursor.fetchone() is None:
            return False, "No existe un producto con ese ID."

        conexion.execute(
            "UPDATE productos SET nombre = ?, precio = ? WHERE id_producto = ?",
            (nuevo_nombre, nuevo_precio, id_producto)
        )

    return True, "Producto actualizado correctamente."


def eliminar_producto(id_producto):
    with conectar() as conexion:

        cursor = conexion.execute(
            "SELECT id_producto FROM productos WHERE id_producto = ?",
            (id_producto,)
        )

        if cursor.fetchone is None:
            return False, "No existe un producto con ese ID."

        conexion.execute(
            "DELETE FROM productos WHERE id_producto = ?",
            (id_producto,)
        )
        
    return True, "Producto eliminado correctamente."