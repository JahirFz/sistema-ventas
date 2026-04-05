from config.database import conectar
from controllers.pago_controller import obtener_estado_venta


def obtener_total_ventas():
    with conectar() as conexion:

        cursor = conexion.execute("""
            SELECT COALESCE(SUM(total), 0)
            FROM ventas
        """)

        return round(cursor.fetchone()[0], 2)


def obtener_total_cobrado():
    with conectar() as conexion:

        cursor = conexion.execute("""
            SELECT COALESCE(SUM(monto), 0)
            FROM pagos
        """)

        return round(cursor.fetchone()[0], 2)


def obtener_total_saldo_pendiente():
    return round(obtener_total_ventas() - obtener_total_cobrado(), 2)


def obtener_conteo_estados():
    with conectar() as conexion:

        cursor = conexion.execute("""
            SELECT id_venta
            FROM ventas
        """)
        ventas = cursor.fetchall()

    pagadas = abonadas = pendientes = 0

    for (id_venta,) in ventas:
        estado = obtener_estado_venta(id_venta)

        if estado == "PAGADA":
            pagadas += 1
        elif estado == "ABONADA":
            abonadas += 1
        elif estado == "PENDIENTE":
            pendientes += 1

    return {
        "pagadas": pagadas,
        "abonadas": abonadas,
        "pendientes": pendientes
    }

