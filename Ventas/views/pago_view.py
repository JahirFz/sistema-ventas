from controllers.pago_controller import (
    agregar_pago,
    listar_pagos,
    listar_pagos_por_venta,
    buscar_pago_por_id,
    eliminar_pago,
    obtener_total_pagado,
    obtener_total_venta,
    obtener_saldo_pendiente,
    obtener_estado_venta
)

def menu_pagos():
    while True:
        print("\n===== MÓDULO DE PAGOS =====")
        print("1. Registrar pago")
        print("2. Listar todos los pagos")
        print("3. Listar pagos por venta")
        print("4. Buscar pago por ID")
        print("5. Eliminar pago")
        print("6. Ver resumen de una venta")
        print("7. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            id_venta = input("Ingresa el ID de la venta:").strip()
            fecha = input("Ingresa la fecha del pago (YYYY-MM-DD): ").strip()
            monto = input("Ingresa el monto del pago: ").strip()
            metodo_pago = input("Ingresa el método de pago: ").strip()

            exito, mensaje = agregar_pago(id_venta, fecha, monto, metodo_pago)
            print(mensaje)

        elif opcion == "2":
            pagos = listar_pagos()

            if not pagos:
                print("No hay pagos registrados.")
            else:
                print("\n--- LISTA DE PAGOS ---")
                for pago in pagos:
                    print(
                        f"ID Pago: {pago[0]} | "
                        f"ID Venta: {pago[1]} | "
                        f"Fecha: {pago[2]} | "
                        f"Monto: ${pago[3]:.2f} | "
                        f"Método: {pago[4]}"
                    )

        elif opcion == "3":
            try:
                id_venta = int(input("Ingresa el ID de la venta: "))
                pagos = listar_pagos_por_venta(id_venta)

                if not pagos:
                    print("No hay pagos registrados para esa venta.")
                else:
                    print("\n--- PAGOS DE LA VENTA ---")
                    for pago in pagos:
                        print(
                            f"ID Pago: {pago[0]} | "
                            f"ID Venta: {pago[1]} | "
                            f"Fecha: {pago[2]} | "
                            f"Monto: ${pago[3]:.2f} | "
                            f"Método: {pago[4]}"
                        )
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "4":
            try:
                id_pago = int(input("Ingresa el ID del pago: "))
                pago = buscar_pago_por_id(id_pago)

                if pago:
                    print(
                        f"ID Pago: {pago[0]} | "
                        f"ID Venta: {pago[1]} | "
                        f"Fecha: {pago[2]} | "
                        f"Monto: ${pago[3]:.2f} | "
                        f"Método: {pago[4]}"
                    )
                else:
                    print("Pago no encontrado.")
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "5":
            try:
                id_pago = int(input("Ingresa el ID del pago a eliminar: "))
                exito, mensaje = eliminar_pago(id_pago)
                print(mensaje)
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "6":
            try:
                id_venta = int(input("Ingresa el ID de la venta: "))

                total_venta = obtener_total_venta(id_venta)
                if total_venta is None:
                    print("No existe una venta con ese ID.")
                else:
                    total_pagado = obtener_total_pagado(id_venta)
                    saldo_pendiente = obtener_saldo_pendiente(id_venta)
                    estado = obtener_estado_venta(id_venta)


                    print("\n--- RESUMEN DE LA VENTA ---")
                    print(f"ID Venta: {id_venta}")
                    print(f"Total de la venta: ${total_venta:.2f}")
                    print(f"Total pagado: ${total_pagado:.2f}")
                    print(f"Saldo pendiente: ${saldo_pendiente:.2f}")
                    print(f"Estado: {estado}")
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "7":
            break

        else:
            print("Opción no válida.")