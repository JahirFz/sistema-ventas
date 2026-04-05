import os
from config.database import (
    crear_tabla_clientes,
    crear_tabla_productos,
    crear_tabla_ventas,
    crear_tabla_detalle_ventas,
    crear_tabla_pagos
)
from gui.app import App

def inicializar_sistema():
    if not os.path.exists("database"):
        os.makedirs("database")
    
    if not os.path.exists("exports"):
        os.makedirs("exports")

    if not os.path.exists("backups"):
        os.makedirs("backups")

    crear_tabla_clientes()
    crear_tabla_productos()
    crear_tabla_ventas()
    crear_tabla_detalle_ventas()
    crear_tabla_pagos()


if __name__ == "__main__":
    inicializar_sistema()

    app = App()
    app.mainloop()