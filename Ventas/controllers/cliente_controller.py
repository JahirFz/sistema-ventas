from config.database import conectar
from utils.validaciones import validar_nombre
import sqlite3

def agregar_cliente(nombre):
    if nombre.strip() == "":
        return False, "El nombre no puede estar vacío."
    
    if not validar_nombre(nombre):
        return False, "El nombre contiene caracteres no permitidos"

    with conectar() as conexion:
        conexion.execute("INSERT INTO clientes (nombre) VALUES (?)", (nombre,))

    return True, "Cliente agregado correctamente."


def listar_clientes():
    with conectar() as conexion:
        cursor = conexion.execute("SELECT id_cliente, nombre FROM clientes")

    return cursor.fetchall()


def buscar_cliente_por_id(id_cliente):
    with conectar() as conexion:
        cursor = conexion.execute("SELECT id_cliente, nombre FROM clientes WHERE id_cliente = ?", (id_cliente,))

    return cursor.fetchone()


def actualizar_cliente(id_cliente, nuevo_nombre):

    if nuevo_nombre.strip() == "":
        return False, "El nombre no puede estar vacío."

    if not validar_nombre(nuevo_nombre):
        return False, "El nombre contiene caracteres no permitidos"   

    with conectar() as conexion:
        cursor = conexion.execute("SELECT id_cliente FROM clientes WHERE id_cliente = ?", (id_cliente,))

        if cursor.fetchone() is None:
            return False, "No existe un cliente con ese ID."

        conexion.execute(
            "UPDATE clientes SET nombre = ? WHERE id_cliente = ?",
            (nuevo_nombre, id_cliente)
        )

    return True, "Cliente actualizado correctamente."


def eliminar_cliente(id_cliente):
    with conectar() as conexion:

        cursor = conexion.execute("SELECT id_cliente FROM clientes WHERE id_cliente = ?", (id_cliente,))

        if cursor.fetchone() is None:
            return False, "No existe un cliente con ese ID."
        try:
            conexion.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
        except sqlite3.IntegrityError:
            return False, "No se puede eliminar el cliente porque tiene ventas registradas."
        
    return True, "Cliente eliminado correctamente."