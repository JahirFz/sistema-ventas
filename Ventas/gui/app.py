import ttkbootstrap as tb
from ttkbootstrap.constants import *
from gui.menu_lateral import MenuLateral
from gui.dashboard_frame_modern import DashboardFrame
from gui.cliente_frame import ClienteFrame
from gui.producto_frame import ProductoFrame
from gui.venta_frame import VentaFrame
from gui.detalle_venta_frame import DetalleVentaFrame
from gui.pago_frame import PagoFrame
from gui.ui_styles import apply_global_styles
from controllers.backup_controller import crear_backup


class App(tb.Window):
    def __init__(self):
        super().__init__(themename="litera")
        apply_global_styles(self)

        self.title("Sistema de Ventas")
        self.geometry("1280x760")
        self.minsize(1100, 680)

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

    def crear_frames(self):
        self.frames["dashboard"] = DashboardFrame(self.contenedor)
        self.frames["clientes"] = ClienteFrame(self.contenedor)
        self.frames["productos"] = ProductoFrame(self.contenedor)
        self.frames["ventas"] = VentaFrame(self.contenedor)
        self.frames["detalle_ventas"] = DetalleVentaFrame(self.contenedor)
        self.frames["pagos"] = PagoFrame(self.contenedor)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def cambiar_vista(self, nombre_vista):
        frame = self.frames[nombre_vista]
        self.menu_lateral.marcar_activa(nombre_vista)

        if hasattr(frame, "actualizar_datos"):
            frame.actualizar_datos()
        frame.tkraise()

    def al_cerrar(self):
        exito, resultado = crear_backup()

        if not exito:
            print(f"Error al crear backup al cerrar: {resultado}")

        self.destroy()
