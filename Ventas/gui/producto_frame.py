import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox

from controllers.producto_controller import (
    agregar_producto,
    listar_productos,
    actualizar_producto,
    eliminar_producto
)


class ProductoFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.id_producto_seleccionado = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_formulario()
        self.crear_tabla()
        self.cargar_productos()

    def actualizar_datos(self):
        self.cargar_productos()

    def crear_formulario(self):
        contenedor = tb.Frame(self)
        contenedor.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        contenedor.grid_columnconfigure(1, weight=1)

        tb.Label(
            contenedor,
            text="Módulo de productos",
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, column=0, columnspan=6, sticky=W, pady=(0, 15))

        tb.Label(contenedor, text="Nombre").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.entry_nombre = tb.Entry(contenedor)
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        tb.Label(contenedor, text="Precio").grid(row=1, column=2, sticky=W, padx=(0, 10))
        self.entry_precio = tb.Entry(contenedor, width=15)
        self.entry_precio.grid(row=1, column=3, sticky=W, padx=(0, 10))

        tb.Button(
            contenedor,
            text="Guardar",
            bootstyle="success",
            command=self.guardar_producto
        ).grid(row=1, column=4, padx=5)

        tb.Button(
            contenedor,
            text="Actualizar",
            bootstyle="warning",
            command=self.editar_producto
        ).grid(row=1, column=5, padx=5)

        tb.Button(
            contenedor,
            text="Limpiar",
            bootstyle="secondary",
            command=self.limpiar_formulario
        ).grid(row=1, column=6, padx=5)

    def crear_tabla(self):
        marco_tabla = tb.Frame(self)
        marco_tabla.grid(row=1, column=0, sticky="nsew")

        columnas = ("id_producto", "nombre", "precio")

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        self.tabla.heading("id_producto", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")

        self.tabla.column("id_producto", width=80, anchor=CENTER)
        self.tabla.column("nombre", width=400, anchor=W)
        self.tabla.column("precio", width=120, anchor=E)

        scrollbar = ttk.Scrollbar(marco_tabla, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        marco_tabla.grid_rowconfigure(0, weight=1)
        marco_tabla.grid_columnconfigure(0, weight=1)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_producto)

        botones = tb.Frame(self)
        botones.grid(row=2, column=0, sticky=W, pady=(10, 0))

        tb.Button(
            botones,
            text="Eliminar seleccionado",
            bootstyle="danger",
            command=self.borrar_producto
        ).pack(side=LEFT)

    def cargar_productos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        productos = listar_productos()

        for producto in productos:
            self.tabla.insert(
                "",
                END,
                values=(producto[0], producto[1], f"${producto[2]:.2f}")
            )

    def guardar_producto(self):
        nombre = self.entry_nombre.get().strip()
        precio = self.entry_precio.get().strip()

        exito, mensaje = agregar_producto(nombre, precio)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_producto(self, event):
        item = self.tabla.selection()
        if not item:
            return

        valores = self.tabla.item(item, "values")
        self.id_producto_seleccionado = int(valores[0])

        self.entry_nombre.delete(0, END)
        self.entry_nombre.insert(0, valores[1])

        precio_limpio = str(valores[2]).replace("$", "").strip()
        self.entry_precio.delete(0, END)
        self.entry_precio.insert(0, precio_limpio)

    def editar_producto(self):
        if self.id_producto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un producto primero.")
            return

        nuevo_nombre = self.entry_nombre.get().strip()
        nuevo_precio = self.entry_precio.get().strip()

        exito, mensaje = actualizar_producto(
            self.id_producto_seleccionado,
            nuevo_nombre,
            nuevo_precio
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def borrar_producto(self):
        if self.id_producto_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un producto primero.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Deseas eliminar este producto?")
        if not confirmar:
            return

        exito, mensaje = eliminar_producto(self.id_producto_seleccionado)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        self.id_producto_seleccionado = None
        self.entry_nombre.delete(0, END)
        self.entry_precio.delete(0, END)
        self.tabla.selection_remove(self.tabla.selection())