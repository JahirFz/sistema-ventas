import ttkbootstrap as tb
from ttkbootstrap.constants import *
from controllers.dashboard_controller import (
    obtener_total_ventas,
    obtener_total_cobrado,
    obtener_total_saldo_pendiente,
    obtener_conteo_estados
)


class DashboardFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        tb.Label(
            self,
            text="Panel principal",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor=W, pady=(0, 20))

        self.tarjetas = tb.Frame(self)
        self.tarjetas.pack(fill=BOTH, expand=True)

        for i in range(3):
            self.tarjetas.grid_columnconfigure(i, weight=1)

        self.card_ventas = self.crear_tarjeta(self.tarjetas, "Ventas totales", "$0.00", "primary")
        self.card_ventas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.card_cobrado = self.crear_tarjeta(self.tarjetas, "Total cobrado", "$0.00", "info")
        self.card_cobrado.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.card_saldo = self.crear_tarjeta(self.tarjetas, "Saldo pendiente", "$0.00", "danger")
        self.card_saldo.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.card_pagadas = self.crear_tarjeta(self.tarjetas, "Ventas pagadas", "0", "success")
        self.card_pagadas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.card_abonadas = self.crear_tarjeta(self.tarjetas, "Ventas abonadas", "0", "warning")
        self.card_abonadas.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.card_pendientes = self.crear_tarjeta(self.tarjetas, "Ventas pendientes", "0", "danger")
        self.card_pendientes.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.actualizar_datos()

    def crear_tarjeta(self, parent, titulo, valor, estilo):
        card = tb.Labelframe(parent, text=titulo, padding=20, bootstyle=estilo)

        etiqueta_valor = tb.Label(
            card,
            text=valor,
            font=("Segoe UI", 18, "bold")
        )
        etiqueta_valor.pack()

        card.etiqueta_valor = etiqueta_valor
        return card

    def actualizar_datos(self):
        total_ventas = obtener_total_ventas()
        total_cobrado = obtener_total_cobrado()
        saldo_pendiente = obtener_total_saldo_pendiente()
        estados = obtener_conteo_estados()

        self.card_ventas.etiqueta_valor.config(text=f"${total_ventas:.2f}")
        self.card_cobrado.etiqueta_valor.config(text=f"${total_cobrado:.2f}")
        self.card_saldo.etiqueta_valor.config(text=f"${saldo_pendiente:.2f}")

        self.card_pagadas.etiqueta_valor.config(text=str(estados["pagadas"]))
        self.card_abonadas.etiqueta_valor.config(text=str(estados["abonadas"]))
        self.card_pendientes.etiqueta_valor.config(text=str(estados["pendientes"]))