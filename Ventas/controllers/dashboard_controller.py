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
            SELECT
                SUM(CASE
                    WHEN COALESCE(p.total_pagado, 0) = 0 THEN 1
                    ELSE 0
                END) AS pendientes,
                SUM(CASE
                    WHEN COALESCE(p.total_pagado, 0) > 0
                     AND COALESCE(p.total_pagado, 0) < v.total THEN 1
                    ELSE 0
                END) AS abonadas,
                SUM(CASE
                    WHEN COALESCE(p.total_pagado, 0) >= v.total THEN 1
                    ELSE 0
                END) AS pagadas
            FROM ventas v
            LEFT JOIN (
                SELECT id_venta, SUM(monto) AS total_pagado
                FROM pagos
                GROUP BY id_venta
            ) p ON v.id_venta = p.id_venta
        """)
        row = cursor.fetchone()

    return {
        "pendientes": row[0] or 0,
        "abonadas":   row[1] or 0,
        "pagadas":    row[2] or 0,
    }

