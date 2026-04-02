from controllers.detalle_venta_controller import (
    agregar_detalle_venta,
    listar_detalle_por_venta,
    eliminar_detalle_venta,
    buscar_detalle_por_id
)

def menu_detalle_ventas():
    while True:
        print("\n===== MÓDULO DE DETALLE DE VENTAS =====")
        print("1. Agregar producto a una venta")
        print("2. Listar detalle de una venta")
        print("3. Buscar detalle por ID")
        print("4. Eliminar detalle")
        print("5. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            id_venta = input("Ingresa el ID de la venta: ").strip()
            id_producto = input("Ingresa el ID del producto: ").strip()
            cantidad = input("Ingresa la cantidad: ").strip()

            exito, mensaje = agregar_detalle_venta(id_venta, id_producto, cantidad)
            print(mensaje)

        elif opcion == "2":
            try:
                id_venta = int(input("Ingresa el ID de la venta: "))
                detalles = listar_detalle_por_venta(id_venta)

                if not detalles:
                    print("No hay detalles registrados para esa venta.")
                else:
                    print("\n--- DETALLE DE LA VENTA ---")
                    for detalle in detalles:
                        print(
                            f"ID Detalle: {detalle[0]} | "
                            f"ID Venta: {detalle[1]} | "
                            f"ID Producto: {detalle[2]} | "
                            f"Producto: {detalle[3]} | "
                            f"Cantidad: {detalle[4]} | "
                            f"Precio Unitario: ${detalle[5]:.2f} | "
                            f"Subtotal: ${detalle[6]:.2f}"
                        )
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "3":
            try:
                id_detalle = int(input("Ingresa el ID del detalle: "))
                detalle = buscar_detalle_por_id(id_detalle)

                if detalle:
                    print(
                        f"ID Detalle: {detalle[0]} | "
                        f"ID Venta: {detalle[1]} | "
                        f"ID Producto: {detalle[2]} | "
                        f"Producto: {detalle[3]} | "
                        f"Cantidad: {detalle[4]} | "
                        f"Precio Unitario: ${detalle[5]:.2f} | "
                        f"Subtotal: ${detalle[6]:.2f}"
                    )
                else:
                    print("Detalle no encontrado.")
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "4":
            try:
                id_detalle = int(input("Ingresa el ID del detalle a eliminar: "))
                exito, mensaje = eliminar_detalle_venta(id_detalle)
                print(mensaje)
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "5":
            break

        else:
            print("Opción no válida.")