import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox

from controllers.venta_controller import listar_ventas
from controllers.producto_controller import listar_productos
from controllers.detalle_venta_controller import (
    agregar_detalle_venta,
    listar_detalle_por_venta,
    eliminar_detalle_venta
)
from controllers.venta_controller import listar_ventas, buscar_venta_por_id


class DetalleVentaFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.id_detalle_seleccionado = None
        self.ventas_dict = {}
        self.productos_dict = {}

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_formulario()
        self.crear_tabla()
        self.crear_resumen()
        self.actualizar_datos()

    def crear_formulario(self):
        contenedor = tb.Frame(self)
        contenedor.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        contenedor.grid_columnconfigure(1, weight=1)

        tb.Label(
            contenedor,
            text="Módulo de detalle de ventas",
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, column=0, columnspan=8, sticky=W, pady=(0, 15))

        tb.Label(contenedor, text="Venta").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.combo_ventas = ttk.Combobox(contenedor, state="readonly", width=40)
        self.combo_ventas.grid(row=1, column=1, sticky=W, padx=(0, 10))
        self.combo_ventas.bind("<<ComboboxSelected>>", self.cambio_venta)

        tb.Label(contenedor, text="Producto").grid(row=1, column=2, sticky=W, padx=(0, 10))
        self.combo_productos = ttk.Combobox(contenedor, state="readonly", width=35)
        self.combo_productos.grid(row=1, column=3, sticky=W, padx=(0, 10))

        tb.Label(contenedor, text="Cantidad").grid(row=1, column=4, sticky=W, padx=(0, 10))
        self.entry_cantidad = tb.Entry(contenedor, width=10)
        self.entry_cantidad.grid(row=1, column=5, sticky=W, padx=(0, 10))

        tb.Button(
            contenedor,
            text="Agregar",
            bootstyle="success",
            command=self.guardar_detalle
        ).grid(row=1, column=6, padx=5)

        tb.Button(
            contenedor,
            text="Limpiar",
            bootstyle="secondary",
            command=self.limpiar_formulario
        ).grid(row=1, column=7, padx=5)

    def crear_tabla(self):
        marco_tabla = tb.Frame(self)
        marco_tabla.grid(row=1, column=0, sticky="nsew")

        columnas = ("id_detalle", "producto", "cantidad", "precio_unitario", "subtotal")

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        self.tabla.heading("id_detalle", text="ID")
        self.tabla.heading("producto", text="Producto")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("precio_unitario", text="Precio unitario")
        self.tabla.heading("subtotal", text="Subtotal")

        self.tabla.column("id_detalle", width=70, anchor=CENTER)
        self.tabla.column("producto", width=300, anchor=W)
        self.tabla.column("cantidad", width=100, anchor=CENTER)
        self.tabla.column("precio_unitario", width=140, anchor=E)
        self.tabla.column("subtotal", width=140, anchor=E)

        scrollbar = ttk.Scrollbar(marco_tabla, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        marco_tabla.grid_rowconfigure(0, weight=1)
        marco_tabla.grid_columnconfigure(0, weight=1)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_detalle)

        botones = tb.Frame(self)
        botones.grid(row=2, column=0, sticky=W, pady=(10, 0))

        tb.Button(
            botones,
            text="Eliminar seleccionado",
            bootstyle="danger",
            command=self.borrar_detalle
        ).pack(side=LEFT)

    def crear_resumen(self):
        marco = tb.Labelframe(self, text="Resumen de la venta", padding=15, bootstyle="info")
        marco.grid(row=3, column=0, sticky=E, pady=(10, 0))

        self.lbl_subtotal = tb.Label(
            marco,
            text="Subtotal de producto: $0.00",
            font=("Segoe UI", 11, "bold")
        )
        self.lbl_subtotal.grid(row=0, column=0, sticky=E, padx=10, pady=2)

        self.lbl_iva = tb.Label(
            marco,
            text="IVA: $0.00",
            font=("Segoe UI", 11, "bold")
        )
        self.lbl_iva.grid(row=1, column=0, sticky=E, padx=10, pady=10)

        self.lbl_total_final = tb.Label(
            marco,
            text="Total final: $0.00",
            font=("Segoe UI", 12, "bold"),
            bootstyle="success"
        )
        self.lbl_total_final.grid(row=2, column=0, sticky=E, padx=10, pady=2)
        
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
            id_venta = venta[0]
            fecha = venta[1]
            cliente = venta[3]
            texto = f"{id_venta} - {cliente} - {fecha}"
            self.ventas_dict[texto] = id_venta
            valores_combo.append(texto)

        self.combo_ventas["values"] = valores_combo

        if seleccion_actual in valores_combo:
            self.combo_ventas.set(seleccion_actual)
        elif valores_combo:
            self.combo_ventas.set(valores_combo[0])

    def cargar_productos(self):
        productos = listar_productos()

        self.productos_dict = {}
        valores_combo = []

        seleccion_actual = self.combo_productos.get().strip()

        for producto in productos:
            id_producto = producto[0]
            nombre = producto[1]
            texto = f"{id_producto} - {nombre}"
            self.productos_dict[texto] = id_producto
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

    def cargar_detalle_actual(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        id_venta = self.obtener_id_venta_actual()

        if id_venta is None:
            self.lbl_total.config(text="Total de la venta: $0.00")
            return

        detalles = listar_detalle_por_venta(id_venta)
        total = 0

        for detalle in detalles:
            subtotal = float(detalle[6])
            total += subtotal

            self.tabla.insert(
                "",
                END,
                values=(
                    detalle[0],
                    detalle[3],
                    detalle[4],
                    f"${detalle[5]:.2f}",
                    f"${detalle[6]:.2f}"
                )
            )

        venta = buscar_venta_por_id(id_venta)

        if venta:
            total_final = float(venta[5])
        else:
            total_final = 0
        iva = total_final - total

        self.lbl_subtotal.config(text=f"Subtotal de productos: ${total:.2f}")
        self.lbl_iva.config(text=f"IVA: ${iva:.2f}")
        self.lbl_total_final.config(text=f"Total final: ${total_final:.2f}")

    def cambio_venta(self, event):
        self.id_detalle_seleccionado = None
        self.cargar_detalle_actual()

    def guardar_detalle(self):
        id_venta = self.obtener_id_venta_actual()
        producto_seleccionado = self.combo_productos.get().strip()
        cantidad = self.entry_cantidad.get().strip()

        if id_venta is None:
            messagebox.showwarning("Aviso", "Selecciona una venta.")
            return

        if producto_seleccionado == "":
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        id_producto = self.productos_dict.get(producto_seleccionado)

        exito, mensaje = agregar_detalle_venta(id_venta, id_producto, cantidad)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.entry_cantidad.delete(0, END)
            self.cargar_detalle_actual()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_detalle(self, event):
        item = self.tabla.selection()
        if not item:
            return

        valores = self.tabla.item(item, "values")
        self.id_detalle_seleccionado = int(valores[0])

    def borrar_detalle(self):
        if self.id_detalle_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un detalle primero.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Deseas eliminar este detalle?")
        if not confirmar:
            return

        exito, mensaje = eliminar_detalle_venta(self.id_detalle_seleccionado)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.id_detalle_seleccionado = None
            self.cargar_detalle_actual()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        self.id_detalle_seleccionado = None
        self.entry_cantidad.delete(0, END)
        self.tabla.selection_remove(self.tabla.selection())