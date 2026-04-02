from controllers.venta_controller import (
    agregar_venta,
    listar_ventas,
    buscar_venta_por_id,
    actualizar_venta,
    eliminar_venta
)

def leer_factura():
    respuesta = input("¿Requiere factura? (s/n): ").strip().lower()

    if respuesta == "s":
        return 1
    elif respuesta == "n":
        return 0
    else:
        return None


def menu_ventas():
    while True:
        print("\n===== MÓDULO DE VENTAS =====")
        print("1. Crear venta")
        print("2. Listar ventas")
        print("3. Buscar venta por ID")
        print("4. Actualizar venta")
        print("5. Eliminar venta")
        print("6. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            fecha = input("Ingresa la fecha de la venta (YYYY-MM-DD): ").strip()
            id_cliente = input("Ingresa el ID del cliente: ").strip()
            requiere_factura = leer_factura()

            if requiere_factura is None:
                print("Debes responder con 's' o 'n'.")
            else:
                exito, mensaje = agregar_venta(fecha, id_cliente, requiere_factura)
                print(mensaje)

        elif opcion == "2":
            ventas = listar_ventas()

            if not ventas:
                print("No hay ventas registradas.")
            else:
                print("\n--- LISTA DE VENTAS ---")
                for venta in ventas:
                    factura_texto = "Sí" if venta[4] == 1 else "No"
                    print(
                        f"ID Venta: {venta[0]} | Fecha: {venta[1]} | "
                        f"ID Cliente: {venta[2]} | Cliente: {venta[3]} | "
                        f"Factura: {factura_texto} | Total: ${venta[5]:.2f}"
                    )

        elif opcion == "3":
            try:
                id_venta = int(input("Ingresa el ID de la venta: "))
                venta = buscar_venta_por_id(id_venta)

                if venta:
                    factura_texto = "Sí" if venta[4] == 1 else "No"
                    print(
                        f"ID Venta: {venta[0]} | Fecha: {venta[1]} | "
                        f"ID Cliente: {venta[2]} | Cliente: {venta[3]} | "
                        f"Factura: {factura_texto} | Total: ${venta[5]:.2f}"
                    )
                else:
                    print("Venta no encontrada.")
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "4":
            try:
                id_venta = int(input("Ingresa el ID de la venta a actualizar: "))
                nueva_fecha = input("Ingresa la nueva fecha (YYYY-MM-DD): ").strip()
                nuevo_id_cliente = input("Ingresa el nuevo ID del cliente: ").strip()
                requiere_factura = leer_factura()

                if requiere_factura is None:
                    print("Debes responder con 's' o 'n'.")
                else:
                    exito, mensaje = actualizar_venta(id_venta, nueva_fecha, nuevo_id_cliente, requiere_factura)
                    print(mensaje)
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "5":
            try:
                id_venta = int(input("Ingresa el ID de la venta a eliminar: "))
                exito, mensaje = eliminar_venta(id_venta)
                print(mensaje)
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "6":
            break

        else:
            print("Opción no válida.")