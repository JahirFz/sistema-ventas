from config.database import conectar
from controllers.pago_controller import obtener_estado_venta


def obtener_total_ventas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM ventas
    """)
    resultado = cursor.fetchone()[0]

    conexion.close()
    return round(resultado, 2)


def obtener_total_cobrado():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(monto), 0)
        FROM pagos
    """)
    resultado = cursor.fetchone()[0]

    conexion.close()
    return round(resultado, 2)


def obtener_total_saldo_pendiente():
    total_ventas = obtener_total_ventas()
    total_cobrado = obtener_total_cobrado()
    return round(total_ventas - total_cobrado, 2)


def obtener_conteo_estados():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_venta
        FROM ventas
    """)
    ventas = cursor.fetchall()

    conexion.close()

    pagadas = 0
    abonadas = 0
    pendientes = 0

    for venta in ventas:
        id_venta = venta[0]
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

def hacer_backup(self):
    ruta = crear_backup()
    messagebox.showinfo("Backup", f"Respaldo creado en:\n{ruta}")