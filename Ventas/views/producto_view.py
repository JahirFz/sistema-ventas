from controllers.producto_controller import (
    agregar_producto,
    listar_productos,
    buscar_producto_por_id,
    actualizar_producto,
    eliminar_producto
)

def menu_productos():
    while True:
        print("\n===== MÓDULO DE PRODUCTOS =====")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Buscar producto por ID")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Volver al menú principal")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nombre = input("Ingresa el nombre del producto: ").strip()
            precio = input("Ingresa el precio del producto: ").strip()

            exito, mensaje = agregar_producto(nombre, precio)
            print(mensaje)

        elif opcion == "2":
            productos = listar_productos()

            if not productos:
                print("No hay productos registrados.")
            else:
                print("\n--- LISTA DE PRODUCTOS ---")
                for producto in productos:
                    print(f"ID: {producto[0]} | Nombre: {producto[1]} | Precio: ${producto[2]:.2f}")

        elif opcion == "3":
            try:
                id_producto = int(input("Ingresa el ID del producto: "))
                producto = buscar_producto_por_id(id_producto)

                if producto:
                    print(f"ID: {producto[0]} | Nombre: {producto[1]} | Precio: ${producto[2]:.2f}")
                else:
                    print("Producto no encontrado.")
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "4":
            try:
                id_producto = int(input("Ingresa el ID del producto a actualizar: "))
                nuevo_nombre = input("Ingresa el nuevo nombre: ").strip()
                nuevo_precio = input("Ingresa el nuevo precio: ").strip()

                exito, mensaje = actualizar_producto(id_producto, nuevo_nombre, nuevo_precio)
                print(mensaje)
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "5":
            try:
                id_producto = int(input("Ingresa el ID del producto a eliminar: "))
                exito, mensaje = eliminar_producto(id_producto)
                print(mensaje)
            except ValueError:
                print("Debes ingresar un número válido.")

        elif opcion == "6":
            break

        else:
            print("Opción no válida.")