import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

from controllers.dashboard_controller import (
    obtener_conteo_estados,
    obtener_total_cobrado,
    obtener_total_saldo_pendiente,
    obtener_total_ventas,
)
from controllers.reporte_controller import (
    exportar_consulta_mesas,
    exportar_consulta_sillas,
    exportar_reporte_mensual,
    exportar_reporte_semanal,
)
from gui.ui_styles import register_metric_card_style


class DashboardFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="App.TFrame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._registrar_estilos_tarjetas()
        self.crear_encabezado()
        self.crear_metricas()
        self.crear_acciones()
        self.actualizar_datos()

    def _registrar_estilos_tarjetas(self):
        style = tb.Style()
        register_metric_card_style(style, "PrimaryMetric", "#163A5F")
        register_metric_card_style(style, "InfoMetric", "#1F5F8B")
        register_metric_card_style(style, "DangerMetric", "#8E3047")
        register_metric_card_style(style, "SuccessMetric", "#177E67")
        register_metric_card_style(style, "WarningMetric", "#A86417")

    def crear_encabezado(self):
        hero = tb.Frame(self, padding=28, style="Surface.TFrame")
        hero.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        hero.grid_columnconfigure(0, weight=1)

        tb.Label(hero, text="Panel principal", style="PageTitle.TLabel").grid(
            row=0, column=0, sticky=W
        )

    def crear_metricas(self):
        self.tarjetas = tb.Frame(self, style="App.TFrame")
        self.tarjetas.grid(row=1, column=0, sticky="nsew")

        for i in range(3):
            self.tarjetas.grid_columnconfigure(i, weight=1)
        for i in range(2):
            self.tarjetas.grid_rowconfigure(i, weight=1)

        self.card_ventas = self.crear_tarjeta(
            self.tarjetas, 0, 0, "Ventas totales", "$0.00", "PrimaryMetric"
        )
        self.card_cobrado = self.crear_tarjeta(
            self.tarjetas, 0, 1, "Total cobrado", "$0.00", "InfoMetric"
        )
        self.card_saldo = self.crear_tarjeta(
            self.tarjetas, 0, 2, "Saldo pendiente", "$0.00", "DangerMetric"
        )
        self.card_pagadas = self.crear_tarjeta(
            self.tarjetas, 1, 0, "Ventas pagadas", "0", "SuccessMetric"
        )
        self.card_abonadas = self.crear_tarjeta(
            self.tarjetas, 1, 1, "Ventas abonadas", "0", "WarningMetric"
        )
        self.card_pendientes = self.crear_tarjeta(
            self.tarjetas, 1, 2, "Ventas pendientes", "0", "DangerMetric"
        )

    def crear_acciones(self):
        acciones = tb.Frame(self, padding=22, style="Surface.TFrame")
        acciones.grid(row=2, column=0, sticky="ew", pady=(18, 0))
        acciones.grid_columnconfigure(0, weight=1)
        acciones.grid_columnconfigure(1, weight=1)
        acciones.grid_columnconfigure(2, weight=1)
        acciones.grid_columnconfigure(3, weight=1)

        tb.Label(
            acciones,
            text="Reportes de ingresos semanales y mensuales.",
            style="SectionSubtitle.TLabel",
        ).grid(row=1, column=0, columnspan=4, sticky=W, pady=(4, 16))

        tb.Button(
            acciones,
            text="Exportar reporte semanal",
            bootstyle="success",
            command=self.exportar_reporte_semanal_gui,
        ).grid(row=2, column=0, sticky="ew", padx=(0, 8))

        tb.Button(
            acciones,
            text="Exportar reporte mensual",
            bootstyle="primary",
            command=self.exportar_reporte_mensual_gui,
        ).grid(row=2, column=1, sticky="ew", padx=8)

        tb.Button(
            acciones,
            text="Consulta de sillas",
            bootstyle="info",
            command=self.exportar_consulta_sillas_gui,
        ).grid(row=2, column=2, sticky="ew", padx=8)

        tb.Button(
            acciones,
            text="Consulta de mesas",
            bootstyle="warning",
            command=self.exportar_consulta_mesas_gui,
        ).grid(row=2, column=3, sticky="ew", padx=(8, 0))

    def crear_tarjeta(self, parent, row, column, titulo, valor, estilo):
        card = tb.Frame(parent, padding=20, style=f"{estilo}.TFrame")
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        tb.Label(card, text=titulo, style=f"{estilo}.Title.TLabel").pack(anchor=W)
        etiqueta_valor = tb.Label(card, text=valor, style=f"{estilo}.Value.TLabel")
        etiqueta_valor.pack(anchor=W, pady=(10, 4))

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

    def exportar_reporte_semanal_gui(self):
        try:
            ruta = exportar_reporte_semanal()
            messagebox.showinfo("Exito", f"Reporte semanal exportado correctamente en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el reporte semanal.\n{e}")

    def exportar_reporte_mensual_gui(self):
        try:
            ruta = exportar_reporte_mensual()
            messagebox.showinfo("Exito", f"Reporte mensual exportado correctamente en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el reporte mensual.\n{e}")

    def exportar_consulta_sillas_gui(self):
        try:
            ruta = exportar_consulta_sillas()
            messagebox.showinfo("Exito", f"Consulta de sillas exportada correctamente en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar la consulta de sillas.\n{e}")

    def exportar_consulta_mesas_gui(self):
        try:
            ruta = exportar_consulta_mesas()
            messagebox.showinfo("Exito", f"Consulta de mesas exportada correctamente en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar la consulta de mesas.\n{e}")
