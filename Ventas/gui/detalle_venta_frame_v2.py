import tkinter as tk
from tkinter import ttk, messagebox

import ttkbootstrap as tb
from ttkbootstrap.constants import *

from controllers.venta_controller import listar_ventas, buscar_venta_por_id
from controllers.producto_controller import listar_productos
from controllers.detalle_venta_controller_v2 import (
    agregar_detalle_venta,
    listar_detalle_por_venta,
    eliminar_detalle_venta,
)
from controllers.pago_controller import obtener_estado_venta


COLOR_OPTIONS = [
    ("Blanco", "#FFFFFF"),
    ("Amarillo", "#FACC15"),
    ("Rojo", "#EF4444"),
    ("Azul", "#3B82F6"),
    ("Verde", "#22C55E"),
    ("Gris", "#6B7280"),
    ("Silver Vein", "#BFC1C2"),
    ("Naranja", "#F97316"),
    ("Vino", "#7F1D1D"),
    ("Cafe", "#8B5E3C"),
]


class DetalleVentaFrame(tb.Frame):
    def __init__(self, parent, abrir_pagos=None):
        super().__init__(parent, style="App.TFrame")

        self.abrir_pagos = abrir_pagos
        self.id_detalle_seleccionado = None
        self.ventas_dict = {}
        self.productos_dict = {}
        self.color_actual = "#FFFFFF"
        self.color_nombre_actual = "Blanco"
        self._imagenes_color = {}

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_formulario()
        self.crear_tabla()
        self.crear_resumen()
        self.actualizar_datos()

    def crear_formulario(self):
        contenedor = tb.Frame(self, padding=20, style="Surface.TFrame")
        contenedor.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        for columna in (1, 3, 4, 5):
            contenedor.grid_columnconfigure(columna, weight=1)

        tb.Label(
            contenedor,
            text="Modulo de detalle de ventas",
            font=("Segoe UI", 20, "bold"),
        ).grid(row=0, column=0, columnspan=8, sticky=W, pady=(0, 15))

        tb.Label(contenedor, text="Venta").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.combo_ventas = ttk.Combobox(contenedor, state="readonly", width=40)
        self.combo_ventas.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        self.combo_ventas.bind("<<ComboboxSelected>>", self.cambio_venta)

        tb.Label(contenedor, text="Producto").grid(row=1, column=2, sticky=W, padx=(0, 10))
        self.combo_productos = ttk.Combobox(contenedor, state="readonly", width=35)
        self.combo_productos.grid(row=1, column=3, sticky="ew", padx=(0, 10))

        tb.Label(contenedor, text="Cantidad").grid(row=1, column=4, sticky=W, padx=(0, 10))
        self.entry_cantidad = tb.Entry(contenedor, width=10)
        self.entry_cantidad.grid(row=1, column=5, sticky=W, padx=(0, 10))

        tb.Label(contenedor, text="Color").grid(row=2, column=0, sticky=W, padx=(0, 10), pady=(12, 0))
        color_frame = tb.Frame(contenedor, style="Surface.TFrame")
        color_frame.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady=(12, 0))

        self.preview_color = tk.Label(
            color_frame,
            bg=self.color_actual,
            width=4,
            height=2,
            relief="solid",
            bd=1,
        )
        self.preview_color.pack(side=LEFT, padx=(0, 8))

        self.combo_colores = ttk.Combobox(
            color_frame,
            state="readonly",
            width=16,
            values=[nombre for nombre, _ in COLOR_OPTIONS],
        )
        self.combo_colores.pack(side=LEFT, padx=(0, 8))
        self.combo_colores.bind("<<ComboboxSelected>>", self.cambio_color)
        self.combo_colores.set(self.color_nombre_actual)

        self.lbl_color = tb.Label(color_frame, text=self.color_actual)
        self.lbl_color.pack(side=LEFT, padx=(0, 8))

        tb.Label(contenedor, text="Leyenda").grid(row=2, column=2, sticky=W, padx=(0, 10), pady=(12, 0))
        self.entry_leyenda = tb.Entry(contenedor)
        self.entry_leyenda.grid(row=2, column=3, columnspan=3, sticky="ew", padx=(0, 10), pady=(12, 0))

        tb.Button(
            contenedor,
            text="Agregar",
            bootstyle="success",
            command=self.guardar_detalle,
        ).grid(row=1, column=6, padx=5)

        tb.Button(
            contenedor,
            text="Limpiar",
            bootstyle="secondary",
            command=self.limpiar_formulario,
        ).grid(row=1, column=7, padx=5)

        tb.Button(
            contenedor,
            text="Ir a pagos",
            bootstyle="info",
            command=self.ir_a_pagos,
        ).grid(row=2, column=7, padx=5, pady=(12, 0))

    def crear_tabla(self):
        marco_tabla = tb.Frame(self, padding=12, style="Surface.TFrame")
        marco_tabla.grid(row=1, column=0, sticky="nsew")

        columnas = ("id_detalle", "producto", "cantidad", "precio_unitario", "subtotal", "leyenda")

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="tree headings",
            height=15,
        )

        self.tabla.heading("#0", text="Color")
        self.tabla.heading("id_detalle", text="ID")
        self.tabla.heading("producto", text="Producto")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("precio_unitario", text="Precio unitario")
        self.tabla.heading("subtotal", text="Subtotal")
        self.tabla.heading("leyenda", text="Leyenda")

        self.tabla.column("#0", width=150, anchor=CENTER)
        self.tabla.column("id_detalle", width=70, anchor=CENTER)
        self.tabla.column("producto", width=220, anchor=W, stretch=True)
        self.tabla.column("cantidad", width=90, anchor=CENTER)
        self.tabla.column("precio_unitario", width=130, anchor=CENTER)
        self.tabla.column("subtotal", width=130, anchor=CENTER)
        self.tabla.column("leyenda", width=240, anchor=W, stretch=True)

        scrollbar = ttk.Scrollbar(marco_tabla, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        marco_tabla.grid_rowconfigure(0, weight=1)
        marco_tabla.grid_columnconfigure(0, weight=1)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_detalle)

        botones = tb.Frame(self, style="App.TFrame")
        botones.grid(row=2, column=0, sticky=W, pady=(10, 0))

        tb.Button(
            botones,
            text="Eliminar seleccionado",
            bootstyle="danger",
            command=self.borrar_detalle,
        ).pack(side=LEFT)

    def crear_resumen(self):
        marco = tb.Labelframe(self, text="Resumen de la venta", padding=15, bootstyle="info")
        marco.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        marco.grid_columnconfigure(0, weight=1)

        self.lbl_subtotal = tb.Label(
            marco, text="Subtotal de producto: $0.00", font=("Segoe UI", 11, "bold")
        )
        self.lbl_subtotal.grid(row=0, column=0, sticky=W, padx=10, pady=2)

        self.lbl_iva = tb.Label(marco, text="IVA: $0.00", font=("Segoe UI", 11, "bold"))
        self.lbl_iva.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.lbl_total_final = tb.Label(
            marco, text="Total final: $0.00", font=("Segoe UI", 12, "bold"), bootstyle="success"
        )
        self.lbl_total_final.grid(row=2, column=0, sticky=W, padx=10, pady=2)

    def actualizar_datos(self):
        self.cargar_ventas()
        self.cargar_productos()
        self.cargar_detalle_actual()

    def cargar_ventas(self):
        ventas = listar_ventas()
        self.ventas_dict = {}
        valores_combo = []

        seleccion_actual = self.combo_ventas.get().strip()

        for venta in ventas:
            texto = f"{venta[0]} - {venta[3]} - {venta[1]}"
            self.ventas_dict[texto] = venta[0]
            valores_combo.append(texto)

        self.combo_ventas["values"] = valores_combo
        if seleccion_actual in valores_combo:
            self.combo_ventas.set(seleccion_actual)
        elif valores_combo:
            self.combo_ventas.set(valores_combo[0])

    def seleccionar_venta_por_id(self, id_venta):
        self.cargar_ventas()

        for texto, venta_id in self.ventas_dict.items():
            if venta_id == id_venta:
                self.combo_ventas.set(texto)
                self.cambio_venta()
                return True

        return False

    def cargar_productos(self):
        productos = listar_productos()
        self.productos_dict = {}
        valores_combo = []

        seleccion_actual = self.combo_productos.get().strip()
        for producto in productos:
            texto = f"{producto[0]} - {producto[1]}"
            self.productos_dict[texto] = producto[0]
            valores_combo.append(texto)

        self.combo_productos["values"] = valores_combo
        if seleccion_actual in valores_combo:
            self.combo_productos.set(seleccion_actual)
        elif valores_combo:
            self.combo_productos.set(valores_combo[0])

    def obtener_id_venta_actual(self):
        venta_seleccionada = self.combo_ventas.get().strip()
        if venta_seleccionada == "":
            return None
        return self.ventas_dict.get(venta_seleccionada)

    def _crear_imagen_color(self, color):
        imagen = tk.PhotoImage(width=28, height=28)
        imagen.put(color, to=(0, 0, 28, 28))
        return imagen

    def _obtener_nombre_color(self, color):
        return next(
            (nombre_color for nombre_color, hex_color in COLOR_OPTIONS if hex_color.upper() == color.upper()),
            color.upper(),
        )

    def cargar_detalle_actual(self):
        self._imagenes_color = {}
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        id_venta = self.obtener_id_venta_actual()
        if id_venta is None:
            self.lbl_subtotal.config(text="Subtotal de productos: $0.00")
            self.lbl_iva.config(text="IVA: $0.00")
            self.lbl_total_final.config(text="Total final: $0.00")
            return

        detalles = listar_detalle_por_venta(id_venta)
        total = 0

        for detalle in detalles:
            subtotal = float(detalle[6])
            total += subtotal

            imagen = self._crear_imagen_color(detalle[7])
            self._imagenes_color[detalle[0]] = imagen

            self.tabla.insert(
                "",
                END,
                text=self._obtener_nombre_color(detalle[7]),
                image=imagen,
                values=(
                    detalle[0],
                    detalle[3],
                    detalle[4],
                    f"${detalle[5]:.2f}",
                    f"${detalle[6]:.2f}",
                    detalle[8],
                ),
            )

        venta = buscar_venta_por_id(id_venta)
        total_final = float(venta[5]) if venta else 0
        iva = total_final - total

        self.lbl_subtotal.config(text=f"Subtotal de productos: ${total:.2f}")
        self.lbl_iva.config(text=f"IVA: ${iva:.2f}")
        self.lbl_total_final.config(text=f"Total final: ${total_final:.2f}")

    def cambio_venta(self, event=None):
        self.id_detalle_seleccionado = None
        self.cargar_detalle_actual()

    def cambio_color(self, event=None):
        nombre = self.combo_colores.get().strip()
        color = next((hex_color for nombre_color, hex_color in COLOR_OPTIONS if nombre_color == nombre), "#FFFFFF")
        self.actualizar_color(color, nombre)

    def actualizar_color(self, color, nombre=None):
        self.color_actual = color.upper()
        if nombre is None:
            nombre = next((nombre_color for nombre_color, hex_color in COLOR_OPTIONS if hex_color == self.color_actual), "Personalizado")
        self.color_nombre_actual = nombre
        self.preview_color.configure(bg=self.color_actual)
        self.lbl_color.configure(text=self.color_nombre_actual)
        self.combo_colores.set(self.color_nombre_actual)

    def guardar_detalle(self):
        id_venta = self.obtener_id_venta_actual()
        producto_seleccionado = self.combo_productos.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        leyenda = self.entry_leyenda.get().strip()

        if id_venta is None:
            messagebox.showwarning("Aviso", "Selecciona una venta.")
            return

        if producto_seleccionado == "":
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        estado = obtener_estado_venta(id_venta)
        if estado == "PAGADA":
            messagebox.showwarning("Aviso", "No puedes modificar una venta que ya esta PAGADA.")
            return

        id_producto = self.productos_dict.get(producto_seleccionado)
        exito, mensaje = agregar_detalle_venta(
            id_venta, id_producto, cantidad, self.color_actual, leyenda
        )

        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.entry_cantidad.delete(0, END)
            self.entry_leyenda.delete(0, END)
            self.actualizar_color("#FFFFFF", "Blanco")
            self.cargar_detalle_actual()
        else:
            messagebox.showerror("Error", mensaje)

    def ir_a_pagos(self):
        id_venta = self.obtener_id_venta_actual()
        if id_venta is None:
            messagebox.showwarning("Aviso", "Selecciona una venta.")
            return

        if self.abrir_pagos is None:
            return

        self.abrir_pagos(id_venta)

    def seleccionar_detalle(self, event):
        item = self.tabla.selection()
        if not item:
            return
        valores = self.tabla.item(item, "values")
        self.id_detalle_seleccionado = int(valores[0])

    def borrar_detalle(self):
        id_venta = self.obtener_id_venta_actual()
        estado = obtener_estado_venta(id_venta)

        if estado == "PAGADA":
            messagebox.showwarning("Aviso", "No puedes modificar una venta que ya esta pagada")
            return

        if self.id_detalle_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un detalle primero.")
            return

        exito, mensaje = eliminar_detalle_venta(self.id_detalle_seleccionado)
        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.id_detalle_seleccionado = None
            self.cargar_detalle_actual()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        self.id_detalle_seleccionado = None
        self.entry_cantidad.delete(0, END)
        self.entry_leyenda.delete(0, END)
        self.actualizar_color("#FFFFFF", "Blanco")
        self.tabla.selection_remove(self.tabla.selection())
