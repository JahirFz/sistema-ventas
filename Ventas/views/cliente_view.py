from controllers.cliente_controller import (
    agregar_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    actualizar_cliente,
    eliminar_cliente
)

def menu_clientes():
    while True:
        print("\n===== MÓDULO DE CLIENTES =====")
        print("1. Agregar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente por ID")
        print("4. Actualizar cliente")
        print("5. Eliminar cliente")
        print("6. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nombre = input("Ingresa el nombre del cliente: ").strip()
            exito, mensaje = agregar_cliente(nombre)
            print(mensaje)

        elif opcion == "2":
            clientes = listar_clientes()

            if not clientes:
                print("No hay clientes registrados.")
            else:
                print("\n--- LISTA DE CLIENTES ---")
                for cliente in clientes:
                    print(f"ID: {cliente[0]} | Nombre: {cliente[1]}")

        elif opcion == "3":
            try:
                id_cliente = int(input("Ingresa el ID del cliente: "))
                cliente = buscar_cliente_por_id(id_cliente)

                if cliente:
                    print(f"ID: {cliente[0]} | Nombre: {cliente[1]}")
                else:
                    print("Cliente no encontrado.")
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "4":
            try:
                id_cliente = int(input("Ingresa el ID del cliente a actualizar: "))
                nuevo_nombre = input("Ingresa el nuevo nombre: ").strip()
                exito, mensaje = actualizar_cliente(id_cliente, nuevo_nombre)
                print(mensaje)
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "5":
            try:
                id_cliente = int(input("Ingresa el ID del cliente a eliminar: "))
                exito, mensaje = eliminar_cliente(id_cliente)
                print(mensaje)
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "6":
            break

        else:
            print("Opción no válida.")