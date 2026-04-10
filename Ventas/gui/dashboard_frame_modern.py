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
        # Colores modernos con gradientes simulados
        register_metric_card_style(style, "PrimaryMetric", "#667EEA")
        register_metric_card_style(style, "InfoMetric", "#4299E1")
        register_metric_card_style(style, "DangerMetric", "#F56565")
        register_metric_card_style(style, "SuccessMetric", "#48BB78")
        register_metric_card_style(style, "WarningMetric", "#ED8936")

    def crear_encabezado(self):
        hero = tb.Frame(self, padding=(32, 28, 32, 20), style="Surface.TFrame")
        hero.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        hero.grid_columnconfigure(0, weight=1)

        tb.Label(hero, text="Panel principal", style="PageTitle.TLabel").grid(
            row=0, column=0, sticky=W
        )
        tb.Label(
            hero, 
            text="Bienvenido al sistema de gestión de ventas", 
            style="PageSubtitle.TLabel"
        ).grid(row=1, column=0, sticky=W, pady=(4, 0))

    def crear_metricas(self):
        container = tb.Frame(self, style="App.TFrame")
        container.grid(row=1, column=0, sticky="nsew", padx=8)

        # Configurar grid 3x2 para las tarjetas
        for i in range(3):
            container.grid_columnconfigure(i, weight=1)
        for i in range(2):
            container.grid_rowconfigure(i, weight=1)

        self.card_ventas = self.crear_tarjeta(
            container, 0, 0, "Ventas totales", "$0.00", "PrimaryMetric", "💰"
        )
        self.card_cobrado = self.crear_tarjeta(
            container, 0, 1, "Total cobrado", "$0.00", "InfoMetric", "💵"
        )
        self.card_saldo = self.crear_tarjeta(
            container, 0, 2, "Saldo pendiente", "$0.00", "DangerMetric", "⚠️"
        )
        self.card_pagadas = self.crear_tarjeta(
            container, 1, 0, "Ventas pagadas", "0", "SuccessMetric", "✅"
        )
        self.card_abonadas = self.crear_tarjeta(
            container, 1, 1, "Ventas abonadas", "0", "WarningMetric", "📋"
        )
        self.card_pendientes = self.crear_tarjeta(
            container, 1, 2, "Ventas pendientes", "0", "DangerMetric", "⏳"
        )

    def crear_acciones(self):
        acciones = tb.Frame(self, padding=(32, 24), style="Surface.TFrame")
        acciones.grid(row=2, column=0, sticky="ew", pady=(16, 0))
        acciones.grid_columnconfigure(0, weight=1)
        acciones.grid_columnconfigure(1, weight=1)
        acciones.grid_columnconfigure(2, weight=1)
        acciones.grid_columnconfigure(3, weight=1)

        tb.Label(
            acciones,
            text="Reportes y consultas rápidas",
            style="SectionTitle.TLabel",
        ).grid(row=0, column=0, columnspan=4, sticky=W, pady=(0, 12))

        tb.Button(
            acciones,
            text="📊 Reporte semanal",
            bootstyle="success-outline",
            command=self.exportar_reporte_semanal_gui,
        ).grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=4)

        tb.Button(
            acciones,
            text="📈 Reporte mensual",
            bootstyle="primary-outline",
            command=self.exportar_reporte_mensual_gui,
        ).grid(row=1, column=1, sticky="ew", padx=8, pady=4)

        tb.Button(
            acciones,
            text="🪑 Consulta sillas",
            bootstyle="info-outline",
            command=self.exportar_consulta_sillas_gui,
        ).grid(row=1, column=2, sticky="ew", padx=8, pady=4)

        tb.Button(
            acciones,
            text="📦 Consulta mesas",
            bootstyle="warning-outline",
            command=self.exportar_consulta_mesas_gui,
        ).grid(row=1, column=3, sticky="ew", padx=(8, 0), pady=4)

    def crear_tarjeta(self, parent, row, column, titulo, valor, estilo, icono=""):
        card = tb.Frame(parent, padding=24, style=f"{estilo}.TFrame")
        card.grid(row=row, column=column, padx=12, pady=12, sticky="nsew")
        
        # Header con ícono y título
        header_frame = tb.Frame(card, style=f"{estilo}.TFrame")
        header_frame.pack(fill=X, anchor=W)
        
        if icono:
            tb.Label(
                header_frame, 
                text=icono, 
                font=("Segoe UI Emoji", 18),
                background=card.cget("background"),
                foreground="#FFFFFF"
            ).pack(side=LEFT, padx=(0, 10))
        
        tb.Label(
            header_frame, 
            text=titulo, 
            style=f"{estilo}.Title.TLabel",
            font=("Segoe UI Semibold", 12)
        ).pack(side=LEFT, fill=X, expand=True)

        etiqueta_valor = tb.Label(
            card, 
            text=valor, 
            style=f"{estilo}.Value.TLabel",
            font=("Segoe UI Semibold", 32)
        )
        etiqueta_valor.pack(anchor=W, pady=(16, 8))

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
