import ttkbootstrap as tb
from ttkbootstrap.constants import *
from gui.ui_styles import PALETTE


class MenuLateral(tb.Frame):
    def __init__(self, parent, comando_cambiar_vista):
        super().__init__(parent, width=260, padding=20, style="Sidebar.TFrame")
        self.grid_propagate(False)
        self.comando_cambiar_vista = comando_cambiar_vista
        self.botones = {}

        encabezado = tb.Frame(self, padding=(10, 12), style="Sidebar.TFrame")
        encabezado.pack(fill=X, pady=(8, 20))

        tb.Label(
            encabezado,
            text="Sistema de Ventas",
            style="SidebarTitle.TLabel"
        ).pack(anchor=W)

        separador = tb.Frame(self, height=1, style="Sidebar.TFrame")
        separador.pack(fill=X, pady=(0, 16))
        separador.configure(borderwidth=0)

        botones = [
            ("Inicio", "dashboard"),
            ("Clientes", "clientes"),
            ("Productos", "productos"),
            ("Ventas", "ventas"),
            ("Detalle ventas", "detalle_ventas"),
            ("Pagos", "pagos"),
        ]

        for texto, vista in botones:
            boton = tb.Button(
                self,
                text=texto,
                style="Sidebar.TButton",
                command=lambda v=vista: self._on_click(v)
            )
            boton.pack(fill=X, pady=4)
            self.botones[vista] = boton

        pie = tb.Frame(self, style="Sidebar.TFrame")
        pie.pack(side=BOTTOM, fill=X, pady=(20, 0))

    def _on_click(self, vista):
        self.marcar_activa(vista)
        self.comando_cambiar_vista(vista)

    def marcar_activa(self, vista_activa):
        for vista, boton in self.botones.items():
            boton.configure(style="SidebarActive.TButton" if vista == vista_activa else "Sidebar.TButton")
