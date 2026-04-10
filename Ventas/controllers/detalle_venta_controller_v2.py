from config.database import conectar
from config.config import IVA
from utils.validaciones import validar_cantidad
import re


def _validar_color_hex(color):
    return re.match(r"^#[0-9A-Fa-f]{6}$", color.strip()) is not None


def recalcular_total_venta(id_venta):
    with conectar() as conexion:
        cursor = conexion.execute(
            """
            SELECT COALESCE(SUM(subtotal), 0)
            FROM detalle_ventas
            WHERE id_venta = ?
            """,
            (id_venta,),
        )
        subtotal_productos = cursor.fetchone()[0] or 0

        cursor = conexion.execute(
            """
            SELECT requiere_factura
            FROM ventas
            WHERE id_venta = ?
            """,
            (id_venta,),
        )
        factura = cursor.fetchone()
        requiere_factura = factura[0] if factura else 0

        total_final = subtotal_productos * (1 + IVA) if requiere_factura == 1 else subtotal_productos
        conexion.execute(
            """
            UPDATE ventas
            SET total = ?
            WHERE id_venta = ?
            """,
            (total_final, id_venta),
        )


def _obtener_factor_total(requiere_factura):
    return 1 + IVA if requiere_factura == 1 else 1


def agregar_detalle_venta(id_venta, id_producto, cantidad, color="#FFFFFF", leyenda=""):
    try:
        id_venta = int(id_venta)
    except ValueError:
        return False, "El ID de la venta debe ser numerico."

    try:
        id_producto = int(id_producto)
    except ValueError:
        return False, "El ID del producto debe ser numerico."

    if not validar_cantidad(cantidad):
        return False, "La cantidad debe ser un numero entero mayor que 0."

    color = color.strip().upper()
    leyenda = leyenda.strip()

    if not _validar_color_hex(color):
        return False, "El color debe tener formato HEX, por ejemplo #FFAA00."

    if len(leyenda) > 120:
        return False, "La leyenda no puede superar 120 caracteres."

    cantidad = int(cantidad)

    with conectar() as conexion:
        cursor = conexion.execute(
            "SELECT id_venta, requiere_factura, total FROM ventas WHERE id_venta = ?",
            (id_venta,),
        )
        venta = cursor.fetchone()
        if venta is None:
            return False, "No existe una venta con ese ID."

        cursor = conexion.execute(
            """
            SELECT id_producto, nombre, precio
            FROM productos
            WHERE id_producto = ?
            """,
            (id_producto,),
        )
        producto = cursor.fetchone()
        if producto is None:
            return False, "No existe un producto con ese ID."

        precio_unitario = producto[2]
        subtotal = cantidad * precio_unitario
        total_incremento = subtotal * _obtener_factor_total(venta[1])

        conexion.execute(
            """
            INSERT INTO detalle_ventas (
                id_venta, id_producto, cantidad, precio_unitario, subtotal, color, leyenda
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (id_venta, id_producto, cantidad, precio_unitario, subtotal, color, leyenda),
        )
        conexion.execute(
            "UPDATE ventas SET total = total + ? WHERE id_venta = ?",
            (total_incremento, id_venta),
        )

    return True, "Producto agregado al detalle de la venta correctamente."


def listar_detalle_por_venta(id_venta):
    with conectar() as conexion:
        cursor = conexion.execute(
            """
            SELECT
                dv.id_detalle,
                dv.id_venta,
                dv.id_producto,
                p.nombre,
                dv.cantidad,
                dv.precio_unitario,
                dv.subtotal,
                dv.color,
                dv.leyenda
            FROM detalle_ventas dv
            INNER JOIN productos p ON dv.id_producto = p.id_producto
            WHERE dv.id_venta = ?
            """,
            (id_venta,),
        )
        return cursor.fetchall()


def eliminar_detalle_venta(id_detalle):
    with conectar() as conexion:
        cursor = conexion.execute(
            """
            SELECT dv.id_detalle, dv.id_venta, dv.subtotal, v.requiere_factura
            FROM detalle_ventas dv
            INNER JOIN ventas v ON dv.id_venta = v.id_venta
            WHERE dv.id_detalle = ?
            """,
            (id_detalle,),
        )
        detalle = cursor.fetchone()
        if detalle is None:
            return False, "No existe un detalle con ese ID."

        id_venta = detalle[1]
        total_decremento = detalle[2] * _obtener_factor_total(detalle[3])
        conexion.execute("DELETE FROM detalle_ventas WHERE id_detalle = ?", (id_detalle,))
        conexion.execute(
            "UPDATE ventas SET total = MAX(total - ?, 0) WHERE id_venta = ?",
            (total_decremento, id_venta),
        )
    return True, "Detalle eliminado correctamente."


def buscar_detalle_por_id(id_detalle):
    with conectar() as conexion:
        cursor = conexion.execute(
            """
            SELECT
                dv.id_detalle,
                dv.id_venta,
                dv.id_producto,
                p.nombre,
                dv.cantidad,
                dv.precio_unitario,
                dv.subtotal,
                dv.color,
                dv.leyenda
            FROM detalle_ventas dv
            INNER JOIN productos p ON dv.id_producto = p.id_producto
            WHERE dv.id_detalle = ?
            """,
            (id_detalle,),
        )
        return cursor.fetchone()


def marcar_detalle_completado(id_detalle, completado=1):
    try:
        id_detalle = int(id_detalle)
    except ValueError:
        return False, "El ID del detalle debe ser numerico."

    with conectar() as conexion:
        cursor = conexion.execute(
            "UPDATE detalle_ventas SET completado = ? WHERE id_detalle = ?",
            (1 if completado else 0, id_detalle),
        )
        if cursor.rowcount == 0:
            return False, "No existe un detalle con ese ID."

    return True, "Detalle marcado como completado correctamente."


def marcar_detalles_completados(ids_detalle, completado=1):
    ids_normalizados = []

    for id_detalle in ids_detalle:
        try:
            ids_normalizados.append(int(id_detalle))
        except ValueError:
            return False, "Todos los IDs de detalle deben ser numericos."

    if not ids_normalizados:
        return True, "No hay detalles para actualizar."

    placeholders = ",".join("?" for _ in ids_normalizados)

    with conectar() as conexion:
        cursor = conexion.execute(
            f"""
            UPDATE detalle_ventas
            SET completado = ?
            WHERE id_detalle IN ({placeholders})
            """,
            (1 if completado else 0, *ids_normalizados),
        )
        if cursor.rowcount == 0:
            return False, "No existe ningun detalle con los IDs proporcionados."

    return True, f"{cursor.rowcount} detalles actualizados correctamente."
