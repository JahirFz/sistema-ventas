import ttkbootstrap as tb
from ttkbootstrap.constants import *
from gui.menu_lateral import MenuLateral
from gui.dashboard_frame_modern import DashboardFrame
from gui.cliente_frame import ClienteFrame
from gui.producto_frame_simple import ProductoFrame
from gui.venta_frame import VentaFrame
from gui.detalle_venta_frame_v2 import DetalleVentaFrame
from gui.pago_frame import PagoFrame
from gui.consultas_frame import ConsultasFrame
from gui.ui_styles import apply_global_styles
from controllers.backup_controller import crear_backup


class App(tb.Window):
    def __init__(self):
        super().__init__(themename="litera")
        apply_global_styles(self)

        self.title("Sistema de Ventas")
        self._configurar_tamano_inicial()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_lateral = MenuLateral(self, self.cambiar_vista)
        self.menu_lateral.grid(row=0, column=0, sticky="ns")

        self.contenedor = tb.Frame(self, padding=24, style="App.TFrame")
        self.contenedor.grid(row=0, column=1, sticky="nsew")

        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.crear_frames()
        self.cambiar_vista("dashboard")

        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

    def _configurar_tamano_inicial(self):
        self.update_idletasks()

        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        ancho = min(1280, max(980, ancho_pantalla - 80))
        alto = min(760, max(640, alto_pantalla - 100))

        x = max((ancho_pantalla - ancho) // 2, 20)
        y = max((alto_pantalla - alto) // 2, 20)

        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.minsize(960, 620)

    def crear_frames(self):
        self.frames["dashboard"] = DashboardFrame(self.contenedor)
        self.frames["clientes"] = ClienteFrame(self.contenedor)
        self.frames["productos"] = ProductoFrame(self.contenedor)
        self.frames["ventas"] = VentaFrame(self.contenedor, self.abrir_detalle_venta)
        self.frames["detalle_ventas"] = DetalleVentaFrame(self.contenedor, self.abrir_pagos)
        self.frames["pagos"] = PagoFrame(self.contenedor, self.abrir_detalle_venta)
        self.frames["consultas"] = ConsultasFrame(self.contenedor)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def cambiar_vista(self, nombre_vista):
        frame = self.frames[nombre_vista]
        self.menu_lateral.marcar_activa(nombre_vista)

        if hasattr(frame, "actualizar_datos"):
            frame.actualizar_datos()
        frame.tkraise()

    def abrir_detalle_venta(self, id_venta):
        self.cambiar_vista("detalle_ventas")
        frame_detalle = self.frames["detalle_ventas"]
        frame_detalle.seleccionar_venta_por_id(id_venta)
        frame_detalle.tkraise()

    def abrir_pagos(self, id_venta):
        self.cambiar_vista("pagos")
        frame_pagos = self.frames["pagos"]
        frame_pagos.seleccionar_venta_por_id(id_venta)
        frame_pagos.tkraise()

    def al_cerrar(self):
        exito, resultado = crear_backup()

        if not exito:
            print(f"Error al crear backup al cerrar: {resultado}")

        self.destroy()
