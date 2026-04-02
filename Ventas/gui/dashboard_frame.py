import ttkbootstrap as tb
from ttkbootstrap.constants import *


class DashboardFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tb.Label(
            self,
            text="Panel principal",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor=W, pady=(0, 20))

        tarjetas = tb.Frame(self)
        tarjetas.pack(fill=X)

        self.crear_tarjeta(tarjetas, "Ventas", "$0.00").grid(row=0, column=0, padx=10, sticky="ew")
        self.crear_tarjeta(tarjetas, "Pagado", "$0.00").grid(row=0, column=1, padx=10, sticky="ew")
        self.crear_tarjeta(tarjetas, "Saldo pendiente", "$0.00").grid(row=0, column=2, padx=10, sticky="ew")

        tarjetas.grid_columnconfigure(0, weight=1)
        tarjetas.grid_columnconfigure(1, weight=1)
        tarjetas.grid_columnconfigure(2, weight=1)

    def crear_tarjeta(self, parent, titulo, valor):
        card = tb.Labelframe(parent, text=titulo, padding=20, bootstyle="info")
        tb.Label(
            card,
            text=valor,
            font=("Segoe UI", 18, "bold")
        ).pack()
        return card