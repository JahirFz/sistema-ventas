import ttkbootstrap as tb
from ttkbootstrap.constants import *


class MenuLateral(tb.Frame):
    def __init__(self, parent, comando_cambiar_vista):
        super().__init__(parent, bootstyle="dark", width=220, padding=15)
        self.grid_propagate(False)

        tb.Label(
            self,
            text="Sistema de Ventas",
            font=("Segoe UI", 16, "bold"),
            bootstyle="inverse-dark"
        ).pack(fill=X, pady=(10, 20))

        botones = [
            ("Inicio", "dashboard"),
            ("Clientes", "clientes"),
            ("Productos", "productos"),
            ("Ventas", "ventas"),
            ("Detalle ventas", "detalle_ventas"),
            ("Pagos", "pagos"),
        ]

        for texto, vista in botones:
            if vista is None:
                boton = tb.Button(
                    self,
                    text=texto,
                    bootstyle="secondary-outline",
                    state="disabled"
                )
            else:
                boton = tb.Button(
                    self,
                    text=texto,
                    bootstyle="secondary",
                    command=lambda v=vista: comando_cambiar_vista(v)
                )

            boton.pack(fill=X, pady=5)