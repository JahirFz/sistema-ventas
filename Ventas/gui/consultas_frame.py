import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, messagebox

from controllers.detalle_venta_controller_v2 import (
    marcar_detalle_completado,
    marcar_detalles_completados,
)
from controllers.reporte_controller import (
    exportar_consulta_mesas,
    exportar_consulta_sillas,
    obtener_consulta_producto_por_categoria,
)


class ConsultasFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="App.TFrame")

        self.categoria_actual = "silla"
        self.modo_completado = 0
        self.detalles_seleccionados = []
        self._imagenes_color = {}

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_encabezado()
        self.crear_tabla()
        self.actualizar_datos()

    def crear_encabezado(self):
        contenedor = tb.Frame(self, padding=20, style="Surface.TFrame")
        contenedor.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        contenedor.grid_columnconfigure(4, weight=1)

        tb.Label(
            contenedor,
            text="Consultas por cliente",
            font=("Segoe UI", 20, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky=W)


        self.btn_sillas = tb.Button(
            contenedor,
            text="Ver sillas",
            bootstyle="primary",
            command=lambda: self.cambiar_categoria("silla"),
        )
        self.btn_sillas.grid(row=2, column=0, padx=(0, 8), sticky=W)

        self.btn_mesas = tb.Button(
            contenedor,
            text="Ver mesas",
            bootstyle="secondary-outline",
            command=lambda: self.cambiar_categoria("mesa"),
        )
        self.btn_mesas.grid(row=2, column=1, padx=8, sticky=W)

        self.btn_exportar = tb.Button(
            contenedor,
            text="Exportar consulta actual",
            bootstyle="success",
            command=self.exportar_consulta_actual,
        )
        self.btn_exportar.grid(row=2, column=2, padx=8, sticky=W)

        self.btn_completar = tb.Button(
            contenedor,
            text="Marcar completado",
            bootstyle="warning",
            command=self.marcar_completado,
        )
        self.btn_completar.grid(row=2, column=3, padx=8, sticky=W)

        self.btn_pendientes = tb.Button(
            contenedor,
            text="Pendientes",
            bootstyle="dark",
            command=lambda: self.cambiar_modo(0),
        )
        self.btn_pendientes.grid(row=3, column=0, padx=(0, 8), pady=(14, 0), sticky=W)

        self.btn_completados = tb.Button(
            contenedor,
            text="Completados",
            bootstyle="secondary-outline",
            command=lambda: self.cambiar_modo(1),
        )
        self.btn_completados.grid(row=3, column=1, padx=8, pady=(14, 0), sticky=W)

        self.lbl_estado = tb.Label(contenedor, text="", style="SectionSubtitle.TLabel")
        self.lbl_estado.grid(row=3, column=4, sticky=E, pady=(14, 0))

    def crear_tabla(self):
        marco_tabla = tb.Frame(self, padding=12, style="Surface.TFrame")
        marco_tabla.grid(row=1, column=0, sticky="nsew")
        marco_tabla.grid_rowconfigure(0, weight=1)
        marco_tabla.grid_columnconfigure(0, weight=1)

        columnas = ("id_detalle", "cliente", "producto", "cantidad", "color", "leyenda")

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            height=18,
            selectmode="extended",
        )

        self.tabla.heading("id_detalle", text="ID")
        self.tabla.heading("cliente", text="Cliente")
        self.tabla.heading("producto", text="Producto")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("color", text="Color")
        self.tabla.heading("leyenda", text="Leyenda")

        self.tabla.column("id_detalle", width=0, stretch=False)
        self.tabla.column("cliente", width=220, anchor=W, stretch=True)
        self.tabla.column("producto", width=200, anchor=W, stretch=True)
        self.tabla.column("cantidad", width=100, anchor=CENTER)
        self.tabla.column("color", width=140, anchor=CENTER)
        self.tabla.column("leyenda", width=240, anchor=W, stretch=True)

        scrollbar = ttk.Scrollbar(marco_tabla, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_detalle)

    def _crear_imagen_color(self, color):
        imagen = tk.PhotoImage(width=28, height=28)
        imagen.put(color, to=(0, 0, 28, 28))
        return imagen

    def cambiar_categoria(self, categoria):
        self.categoria_actual = categoria
        self.btn_sillas.configure(bootstyle="primary" if categoria == "silla" else "secondary-outline")
        self.btn_mesas.configure(bootstyle="primary" if categoria == "mesa" else "secondary-outline")
        self.actualizar_datos()

    def cambiar_modo(self, completado):
        self.modo_completado = completado
        self.btn_pendientes.configure(bootstyle="dark" if completado == 0 else "secondary-outline")
        self.btn_completados.configure(bootstyle="dark" if completado == 1 else "secondary-outline")
        self.btn_completar.configure(
            text="Marcar completado" if completado == 0 else "Reactivar pedido",
            bootstyle="warning" if completado == 0 else "success",
        )
        self.actualizar_datos()

    def actualizar_datos(self):
        registros = obtener_consulta_producto_por_categoria(
            self.categoria_actual, completado=self.modo_completado
        )
        self.detalles_seleccionados = []
        self._imagenes_color = {}

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for registro in registros:
            self.tabla.insert(
                "",
                END,
                values=(
                    registro["id_detalle"],
                    registro["cliente"],
                    registro["producto"],
                    registro["cantidad"],
                    registro["color"],
                    registro["leyenda"],
                ),
            )

        titulo = "sillas" if self.categoria_actual == "silla" else "mesas"
        estado = "completados" if self.modo_completado == 1 else "pendientes"
        self.lbl_estado.configure(text=f"{len(registros)} registros de {titulo} {estado}")

    def seleccionar_detalle(self, event):
        items = self.tabla.selection()
        if not items:
            self.detalles_seleccionados = []
            return

        self.detalles_seleccionados = [
            int(self.tabla.item(item, "values")[0])
            for item in items
        ]

    def exportar_consulta_actual(self):
        try:
            if self.categoria_actual == "silla":
                ruta = exportar_consulta_sillas(completado=self.modo_completado)
                texto = "Consulta de sillas"
            else:
                ruta = exportar_consulta_mesas(completado=self.modo_completado)
                texto = "Consulta de mesas"

            estado = "completados" if self.modo_completado == 1 else "pendientes"
            messagebox.showinfo("Exito", f"{texto} ({estado}) exportada correctamente en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar la consulta actual.\n{e}")

    def marcar_completado(self):
        if not self.detalles_seleccionados:
            messagebox.showwarning("Aviso", "Selecciona uno o mas registros primero.")
            return

        cantidad = len(self.detalles_seleccionados)
        confirmar = messagebox.askyesno(
            "Confirmar",
            (
                f"Se marcaran {cantidad} registros como completados y dejaran de aparecer en pendientes. Deseas continuar?"
                if self.modo_completado == 0
                else f"Se reactivaran {cantidad} registros y volveran a aparecer en pendientes. Deseas continuar?"
            ),
        )
        if not confirmar:
            return

        completado_destino = 0 if self.modo_completado == 1 else 1
        if cantidad == 1:
            exito, mensaje = marcar_detalle_completado(
                self.detalles_seleccionados[0], completado=completado_destino
            )
        else:
            exito, mensaje = marcar_detalles_completados(
                self.detalles_seleccionados, completado=completado_destino
            )

        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", mensaje)
