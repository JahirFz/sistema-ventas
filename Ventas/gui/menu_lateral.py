import ttkbootstrap as tb
from ttkbootstrap.constants import *
from gui.ui_styles import PALETTE


class MenuLateral(tb.Frame):
    def __init__(self, parent, comando_cambiar_vista):
        super().__init__(parent, width=260, padding=(16, 24), style="Sidebar.TFrame")
        self.grid_propagate(False)
        self.comando_cambiar_vista = comando_cambiar_vista
        self.botones = {}

        # Encabezado con logo/icono
        encabezado = tb.Frame(self, padding=(16, 20), style="Sidebar.TFrame")
        encabezado.pack(fill=X, pady=(8, 24))

        # Icono o logo simulado
        logo_label = tb.Label(
            encabezado,
            text="🏪",
            font=("Segoe UI Emoji", 32),
            background=PALETTE["sidebar"],
            foreground="#FFFFFF"
        )
        logo_label.pack(anchor=W, padx=(4, 0))

        tb.Label(
            encabezado,
            text="Sistema de Ventas",
            style="SidebarTitle.TLabel"
        ).pack(anchor=W, pady=(8, 0))

        tb.Label(
            encabezado,
            text="Gestión comercial",
            font=("Segoe UI", 11),
            background=PALETTE["sidebar"],
            foreground="#94A3B8"
        ).pack(anchor=W)

        # Separador sutil
        separador = tb.Frame(
            self, 
            height=1, 
            background="#1E293B",
            borderwidth=0
        )
        separador.pack(fill=X, pady=(12, 20))

        botones = [
            ("📊 Inicio", "dashboard"),
            ("👥 Clientes", "clientes"),
            ("📦 Productos", "productos"),
            ("🛒 Ventas", "ventas"),
            ("📋 Detalle ventas", "detalle_ventas"),
            ("💳 Pagos", "pagos"),
            ("🔍 Consultas", "consultas"),
        ]

        for texto, vista in botones:
            btn_container = tb.Frame(self, style="Sidebar.TFrame")
            btn_container.pack(fill=X, pady=3)
            
            boton = tb.Button(
                btn_container,
                text=texto,
                style="Sidebar.TButton",
                command=lambda v=vista: self._on_click(v)
            )
            boton.pack(fill=X)
            self.botones[vista] = boton

        # Pie del sidebar
        pie = tb.Frame(self, style="Sidebar.TFrame")
        pie.pack(side=BOTTOM, fill=X, pady=(24, 0))
        
        tb.Label(
            pie,
            text="v2.0",
            font=("Segoe UI", 9),
            background=PALETTE["sidebar"],
            foreground="#475569"
        ).pack(anchor=W, padx=16)

    def _on_click(self, vista):
        self.marcar_activa(vista)
        self.comando_cambiar_vista(vista)

    def marcar_activa(self, vista_activa):
        for vista, boton in self.botones.items():
            boton.configure(style="SidebarActive.TButton" if vista == vista_activa else "Sidebar.TButton")
