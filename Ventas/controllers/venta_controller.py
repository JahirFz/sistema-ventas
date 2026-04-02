from config.database import conectar
from utils.validaciones import validar_fecha
from controllers.detalle_venta_controller import recalcular_total_venta

def agregar_venta(fecha, id_cliente, requiere_factura):
    fecha = fecha.strip()

    if fecha == "":
        return False, "La fecha no puede estar vacía."

    if not validar_fecha(fecha):
        return False, "La fecha no tiene un formato válido. Usa YYYY-MM-DD."

    try:
        id_cliente = int(id_cliente)
    except ValueError:
        return False, "El ID del cliente debe ser numérico."

    if requiere_factura not in[0, 1]:
        return False, "El valor de factura no es valido"
    
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_cliente FROM clientes WHERE id_cliente = ?",
        (id_cliente,)
    )
    cliente = cursor.fetchone()

    if cliente is None:
        conexion.close()
        return False, "No existe un cliente con ese ID."

    cursor.execute(
        "INSERT INTO ventas (fecha, id_cliente, requiere_factura, total) VALUES (?, ?, ?, ?)",
        (fecha, id_cliente, requiere_factura, 0)
    )

    conexion.commit()
    conexion.close()

    return True, "Venta registrada correctamente con total inicial en 0."


def listar_ventas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT v.id_venta, v.fecha, v.id_cliente, c.nombre, v.requiere_factura, v.total
        FROM ventas v
        INNER JOIN clientes c ON v.id_cliente = c.id_cliente
    """)
    ventas = cursor.fetchall()

    conexion.close()
    return ventas


def buscar_venta_por_id(id_venta):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT v.id_venta, v.fecha, v.id_cliente, c.nombre, v.requiere_factura, v.total
        FROM ventas v
        INNER JOIN clientes c ON v.id_cliente = c.id_cliente
        WHERE v.id_venta = ?
    """, (id_venta,))
    venta = cursor.fetchone()

    conexion.close()
    return venta


def actualizar_venta(id_venta, nueva_fecha, nuevo_id_cliente, requiere_factura):
    nueva_fecha = nueva_fecha.strip()

    if nueva_fecha == "":
        return False, "La fecha no puede estar vacía."

    if not validar_fecha(nueva_fecha):
        return False, "La fecha no tiene un formato válido. Usa YYYY-MM-DD."

    try:
        id_venta = int(id_venta)
    except ValueError:
        return False, "El ID de la venta debe ser numérico."

    try:
        nuevo_id_cliente = int(nuevo_id_cliente)
    except ValueError:
        return False, "El ID del cliente debe ser numérico."

    if requiere_factura not in [0, 1]:
        return False, "El valor de factura no es valido"
    
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_venta FROM ventas WHERE id_venta = ?",
        (id_venta,)
    )
    venta = cursor.fetchone()

    if venta is None:
        conexion.close()
        return False, "No existe una venta con ese ID."

    cursor.execute(
        "SELECT id_cliente FROM clientes WHERE id_cliente = ?",
        (nuevo_id_cliente,)
    )
    cliente = cursor.fetchone()

    if cliente is None:
        conexion.close()
        return False, "No existe un cliente con ese ID."

    cursor.execute("""
        UPDATE ventas
        SET fecha = ?, id_cliente = ?, requiere_factura = ?
        WHERE id_venta = ?
    """, (nueva_fecha, nuevo_id_cliente, requiere_factura, id_venta))

    conexion.commit()
    conexion.close()

    recalcular_total_venta(id_venta)

    return True, "Venta actualizada correctamente."


def eliminar_venta(id_venta):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_venta FROM ventas WHERE id_venta = ?",
        (id_venta,)
    )
    venta = cursor.fetchone()

    if venta is None:
        conexion.close()
        return False, "No existe una venta con ese ID."

    cursor.execute(
        "DELETE FROM ventas WHERE id_venta = ?",
        (id_venta,)
    )

    conexion.commit()
    conexion.close()

    return True, "Venta eliminada correctamente."