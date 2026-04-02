from config.database import conectar
from utils.validaciones import validar_fecha, validar_total, validar_metodo_pago

def obtener_total_pagado(id_venta):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(monto), 0)
        FROM pagos
        WHERE id_venta = ?
    """, (id_venta,))
    resultado = cursor.fetchone()

    conexion.close()
    return round(resultado[0], 2) if resultado else 0


def obtener_total_venta(id_venta):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT total
        FROM ventas
        WHERE id_venta = ?
    """, (id_venta,))
    resultado = cursor.fetchone()

    conexion.close()
    return round(resultado[0], 2) if resultado else None


def obtener_saldo_pendiente(id_venta):
    total_venta = obtener_total_venta(id_venta)

    if total_venta is None:
        return None

    total_pagado = obtener_total_pagado(id_venta)
    saldo = total_venta - total_pagado

    return round(saldo, 2)


def agregar_pago(id_venta, fecha, monto, metodo_pago):
    fecha = fecha.strip()
    metodo_pago = metodo_pago.strip()

    try:
        id_venta = int(id_venta)
    except ValueError:
        return False, "El ID de la venta debe ser numérico."

    if fecha == "":
        return False, "La fecha no puede estar vacía."

    if not validar_fecha(fecha):
        return False, "La fecha no tiene un formato válido. Usa YYYY-MM-DD."

    if not validar_total(monto):
        return False, "El monto debe ser numérico y mayor que 0."

    if not validar_metodo_pago(metodo_pago):
        return False, "El método de pago contiene caracteres no permitidos."

    monto = round(float(monto), 2)

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_venta, total
        FROM ventas
        WHERE id_venta = ?
    """, (id_venta,))
    venta = cursor.fetchone()

    if venta is None:
        conexion.close()
        return False, "No existe una venta con ese ID."

    total_venta = round(venta[1], 2)

    cursor.execute("""
        SELECT COALESCE(SUM(monto), 0)
        FROM pagos
        WHERE id_venta = ?
    """, (id_venta,))
    total_pagado_actual = round(cursor.fetchone()[0], 2)

    saldo_pendiente = round(total_venta - total_pagado_actual, 2)

    if monto > saldo_pendiente:
        conexion.close()
        return False, f"El monto excede el saldo pendiente de ${saldo_pendiente:.2f}."

    cursor.execute("""
        INSERT INTO pagos (id_venta, fecha, monto, metodo_pago)
        VALUES (?, ?, ?, ?)
    """, (id_venta, fecha, monto, metodo_pago))

    conexion.commit()
    conexion.close()

    return True, "Pago registrado correctamente."


def listar_pagos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            p.id_pago,
            p.id_venta,
            p.fecha,
            p.monto,
            p.metodo_pago
        FROM pagos p
    """)
    pagos = cursor.fetchall()

    conexion.close()
    return pagos


def listar_pagos_por_venta(id_venta):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            id_pago,
            id_venta,
            fecha,
            monto,
            metodo_pago
        FROM pagos
        WHERE id_venta = ?
    """, (id_venta,))
    pagos = cursor.fetchall()

    conexion.close()
    return pagos


def buscar_pago_por_id(id_pago):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            id_pago,
            id_venta,
            fecha,
            monto,
            metodo_pago
        FROM pagos
        WHERE id_pago = ?
    """, (id_pago,))
    pago = cursor.fetchone()

    conexion.close()
    return pago


def eliminar_pago(id_pago):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_pago
        FROM pagos
        WHERE id_pago = ?
    """, (id_pago,))
    pago = cursor.fetchone()

    if pago is None:
        conexion.close()
        return False, "No existe un pago con ese ID."

    cursor.execute("""
        DELETE FROM pagos
        WHERE id_pago = ?
    """, (id_pago,))

    conexion.commit()
    conexion.close()

    return True, "Pago eliminado correctamente."


def obtener_estado_venta(id_venta):

    total_venta = obtener_total_venta(id_venta)

    if total_venta is None:
        return None

    total_pagado = obtener_total_pagado(id_venta)

    if total_pagado == 0:
        return "PENDIENTE"

    elif total_pagado < total_venta:
        return "ABONADA"

    else:
        return "PAGADA"