from config.database import conectar
from utils.validaciones import validar_nombre

def agregar_cliente(nombre):
    if nombre.strip() == "":
        return False, "El nombre no puede estar vacío."
    
    if not validar_nombre(nombre):
        return False, "El nombre contiene caracteres no permitidos"

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO clientes (nombre) VALUES (?)", (nombre,))
    conexion.commit()
    conexion.close()

    return True, "Cliente agregado correctamente."


def listar_clientes():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_cliente, nombre FROM clientes")
    clientes = cursor.fetchall()

    conexion.close()
    return clientes


def buscar_cliente_por_id(id_cliente):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_cliente, nombre FROM clientes WHERE id_cliente = ?", (id_cliente,))
    cliente = cursor.fetchone()

    conexion.close()
    return cliente


def actualizar_cliente(id_cliente, nuevo_nombre):

    if nuevo_nombre.strip() == "":
        return False, "El nombre no puede estar vacío."

    if not validar_nombre(nuevo_nombre):
        return False, "El nombre contiene caracteres no permitidos"   

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_cliente FROM clientes WHERE id_cliente = ?", (id_cliente,))
    cliente = cursor.fetchone()

    if cliente is None:
        conexion.close()
        return False, "No existe un cliente con ese ID."

    cursor.execute(
        "UPDATE clientes SET nombre = ? WHERE id_cliente = ?",
        (nuevo_nombre, id_cliente)
    )

    conexion.commit()
    conexion.close()

    return True, "Cliente actualizado correctamente."


def eliminar_cliente(id_cliente):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_cliente FROM clientes WHERE id_cliente = ?", (id_cliente,))
    cliente = cursor.fetchone()

    if cliente is None:
        conexion.close()
        return False, "No existe un cliente con ese ID."

    cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
    conexion.commit()
    conexion.close()

    return True, "Cliente eliminado correctamente."