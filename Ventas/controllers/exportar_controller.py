import os
from openpyxl import Workbook
from config.database import conectar
from controllers.pago_controller import obtener_estado_venta


def crear_carpeta_exports():
    if not os.path.exists("exports"):
        os.makedirs("exports")


def exportar_ventas_excel():
    crear_carpeta_exports()

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            v.id_venta,
            v.fecha,
            c.nombre,
            v.requiere_factura,
            v.total
        FROM ventas v
        INNER JOIN clientes c ON v.id_cliente = c.id_cliente
        ORDER BY v.id_venta
    """)
    ventas = cursor.fetchall()
    conexion.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Ventas"

    encabezados = ["ID Venta", "Fecha", "Cliente", "Factura", "Total", "Estado"]
    ws.append(encabezados)

    for venta in ventas:
        id_venta = venta[0]
        fecha = venta[1]
        cliente = venta[2]
        factura = "Sí" if venta[3] == 1 else "No"
        total = float(venta[4])
        estado = obtener_estado_venta(id_venta)

        ws.append([id_venta, fecha, cliente, factura, total, estado])

    for columna in ws.columns:
        max_length = 0
        letra_columna = columna[0].column_letter

        for celda in columna:
            if celda.value is not None:
                max_length = max(max_length, len(str(celda.value)))

        ws.column_dimensions[letra_columna].width = max_length + 2

    ruta_archivo = os.path.join("exports", "ventas.xlsx")
    wb.save(ruta_archivo)

    return ruta_archivo


def exportar_pagos_excel():
    crear_carpeta_exports()

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
        ORDER BY p.id_pago
    """)
    pagos = cursor.fetchall()
    conexion.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Pagos"

    encabezados = ["ID Pago", "ID Venta", "Fecha", "Monto", "Método de pago"]
    ws.append(encabezados)

    for pago in pagos:
        ws.append([
            pago[0],
            pago[1],
            pago[2],
            float(pago[3]),
            pago[4]
        ])

    for columna in ws.columns:
        max_length = 0
        letra_columna = columna[0].column_letter

        for celda in columna:
            if celda.value is not None:
                max_length = max(max_length, len(str(celda.value)))

        ws.column_dimensions[letra_columna].width = max_length + 2

    ruta_archivo = os.path.join("exports", "pagos.xlsx")
    wb.save(ruta_archivo)

    return ruta_archivo