from config.database import conectar
from utils.validaciones import validar_cantidad

def recalcular_total_venta(id_venta):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(subtotal), 0)
        FROM detalle_ventas
        WHERE id_venta = ?
    """, (id_venta,))
    resultado = cursor.fetchone()

    subtotal_productos = resultado[0] if resultado else 0

    cursor.execute("""
        SELECT requiere_factura
        FROM ventas
        WHERE id_venta = ?
    """, (id_venta,))
    factura = cursor.fetchone()

    requiere_factura = factura[0] if factura else 0

    if requiere_factura == 1:
        total_final = subtotal_productos * 1.16
    else:
        total_final = subtotal_productos

    cursor.execute("""
        UPDATE ventas
        SET total = ?
        WHERE id_venta = ?
    """, (total_final, id_venta))

    conexion.commit()
    conexion.close()


def agregar_detalle_venta(id_venta, id_producto, cantidad):
    try:
        id_venta = int(id_venta)
    except ValueError:
        return False, "El ID de la venta debe ser numérico."

    try:
        id_producto = int(id_producto)
    except ValueError:
        return False, "El ID del producto debe ser numérico."

    if not validar_cantidad(cantidad):
        return False, "La cantidad debe ser un número entero mayor que 0."

    cantidad = int(cantidad)

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_venta FROM ventas WHERE id_venta = ?", (id_venta,))
    venta = cursor.fetchone()

    if venta is None:
        conexion.close()
        return False, "No existe una venta con ese ID."

    cursor.execute("""
        SELECT id_producto, nombre, precio
        FROM productos
        WHERE id_producto = ?
    """, (id_producto,))
    producto = cursor.fetchone()

    if producto is None:
        conexion.close()
        return False, "No existe un producto con ese ID."

    precio_unitario = producto[2]
    subtotal = cantidad * precio_unitario

    cursor.execute("""
        INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
    """, (id_venta, id_producto, cantidad, precio_unitario, subtotal))

    conexion.commit()
    conexion.close()

    recalcular_total_venta(id_venta)

    return True, "Producto agregado al detalle de la venta correctamente."


def listar_detalle_por_venta(id_venta):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            dv.id_detalle,
            dv.id_venta,
            dv.id_producto,
            p.nombre,
            dv.cantidad,
            dv.precio_unitario,
            dv.subtotal
        FROM detalle_ventas dv
        INNER JOIN productos p ON dv.id_producto = p.id_producto
        WHERE dv.id_venta = ?
    """, (id_venta,))
    detalles = cursor.fetchall()

    conexion.close()
    return detalles


def eliminar_detalle_venta(id_detalle):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_detalle, id_venta
        FROM detalle_ventas
        WHERE id_detalle = ?
    """, (id_detalle,))
    detalle = cursor.fetchone()

    if detalle is None:
        conexion.close()
        return False, "No existe un detalle con ese ID."

    id_venta = detalle[1]

    cursor.execute("""
        DELETE FROM detalle_ventas
        WHERE id_detalle = ?
    """, (id_detalle,))

    conexion.commit()
    conexion.close()

    recalcular_total_venta(id_venta)

    return True, "Detalle eliminado correctamente."


def buscar_detalle_por_id(id_detalle):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            dv.id_detalle,
            dv.id_venta,
            dv.id_producto,
            p.nombre,
            dv.cantidad,
            dv.precio_unitario,
            dv.subtotal
        FROM detalle_ventas dv
        INNER JOIN productos p ON dv.id_producto = p.id_producto
        WHERE dv.id_detalle = ?
    """, (id_detalle,))
    detalle = cursor.fetchone()

    conexion.close()
    return detalle