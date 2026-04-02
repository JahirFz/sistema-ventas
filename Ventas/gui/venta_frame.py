import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox
from datetime import date

from controllers.venta_controller import (
    agregar_venta,
    listar_ventas,
    actualizar_venta,
    eliminar_venta
)
from controllers.cliente_controller import listar_clientes


class VentaFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.id_venta_seleccionada = None
        self.clientes_dict = {}

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_formulario()
        self.crear_tabla()
        self.cargar_clientes()
        self.cargar_ventas()
        self.colocar_fecha_hoy()

    def actualizar_datos(self):
        self.cargar_clientes()
        self.cargar_ventas()

        if self.id_venta_seleccionada is None:
            self.colocar_fecha_hoy()
        
    def crear_formulario(self):
        contenedor = tb.Frame(self)
        contenedor.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        contenedor.grid_columnconfigure(1, weight=1)

        tb.Label(
            contenedor,
            text="Módulo de ventas",
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, column=0, columnspan=8, sticky=W, pady=(0, 15))

        tb.Label(contenedor, text="Fecha").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.entry_fecha = tb.Entry(contenedor, width=15)
        self.entry_fecha.grid(row=1, column=1, sticky=W, padx=(0, 10))

        tb.Label(contenedor, text="Cliente").grid(row=1, column=2, sticky=W, padx=(0, 10))
        self.combo_clientes = ttk.Combobox(contenedor, state="readonly", width=30)
        self.combo_clientes.grid(row=1, column=3, sticky=W, padx=(0, 10))

        self.var_factura = tb.IntVar(value=0)
        self.check_factura = tb.Checkbutton(
            contenedor,
            text="Requiere factura",
            variable=self.var_factura,
            bootstyle="round-toggle"
        )
        self.check_factura.grid(row=1, column=4, sticky=W, padx=(0, 10))

        tb.Button(
            contenedor,
            text="Guardar",
            bootstyle="success",
            command=self.guardar_venta
        ).grid(row=1, column=5, padx=5)

        tb.Button(
            contenedor,
            text="Actualizar",
            bootstyle="warning",
            command=self.editar_venta
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

        columnas = ("id_venta", "fecha", "cliente", "factura", "total")

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        self.tabla.heading("id_venta", text="ID")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("cliente", text="Cliente")
        self.tabla.heading("factura", text="Factura")
        self.tabla.heading("total", text="Total")

        self.tabla.column("id_venta", width=70, anchor=CENTER)
        self.tabla.column("fecha", width=120, anchor=CENTER)
        self.tabla.column("cliente", width=300, anchor=W)
        self.tabla.column("factura", width=100, anchor=CENTER)
        self.tabla.column("total", width=120, anchor=E)

        scrollbar = ttk.Scrollbar(marco_tabla, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        marco_tabla.grid_rowconfigure(0, weight=1)
        marco_tabla.grid_columnconfigure(0, weight=1)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_venta)

        botones = tb.Frame(self)
        botones.grid(row=2, column=0, sticky=W, pady=(10, 0))

        tb.Button(
            botones,
            text="Eliminar seleccionada",
            bootstyle="danger",
            command=self.borrar_venta
        ).pack(side=LEFT)

    def cargar_clientes(self):
        clientes = listar_clientes()

        self.clientes_dict = {}
        nombres_clientes = []

        for cliente in clientes:
            id_cliente = cliente[0]
            nombre = cliente[1]
            texto = f"{id_cliente} - {nombre}"
            self.clientes_dict[texto] = id_cliente
            nombres_clientes.append(texto)

        self.combo_clientes["values"] = nombres_clientes

    def cargar_ventas(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        ventas = listar_ventas()

        for venta in ventas:
            factura_texto = "Sí" if venta[4] == 1 else "No"

            self.tabla.insert(
                "",
                END,
                values=(
                    venta[0],
                    venta[1],
                    venta[3],
                    factura_texto,
                    f"${venta[5]:.2f}"
                )
            )

    def guardar_venta(self):
        fecha = self.entry_fecha.get().strip()
        cliente_seleccionado = self.combo_clientes.get().strip()
        requiere_factura = self.var_factura.get()

        if cliente_seleccionado == "":
            messagebox.showwarning("Aviso", "Selecciona un cliente.")
            return

        id_cliente = self.clientes_dict.get(cliente_seleccionado)

        exito, mensaje = agregar_venta(fecha, id_cliente, requiere_factura)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_ventas()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_venta(self, event):
        item = self.tabla.selection()
        if not item:
            return

        valores = self.tabla.item(item, "values")
        self.id_venta_seleccionada = int(valores[0])

        self.entry_fecha.delete(0, END)
        self.entry_fecha.insert(0, valores[1])

        nombre_cliente = valores[2]
        for texto, id_cliente in self.clientes_dict.items():
            if texto.endswith(f"- {nombre_cliente}"):
                self.combo_clientes.set(texto)
                break

        self.var_factura.set(1 if valores[3] == "Sí" else 0)

    def editar_venta(self):
        if self.id_venta_seleccionada is None:
            messagebox.showwarning("Aviso", "Selecciona una venta primero.")
            return

        fecha = self.entry_fecha.get().strip()
        cliente_seleccionado = self.combo_clientes.get().strip()
        requiere_factura = self.var_factura.get()

        if cliente_seleccionado == "":
            messagebox.showwarning("Aviso", "Selecciona un cliente.")
            return

        id_cliente = self.clientes_dict.get(cliente_seleccionado)

        exito, mensaje = actualizar_venta(
            self.id_venta_seleccionada,
            fecha,
            id_cliente,
            requiere_factura
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_ventas()
        else:
            messagebox.showerror("Error", mensaje)

    def borrar_venta(self):
        if self.id_venta_seleccionada is None:
            messagebox.showwarning("Aviso", "Selecciona una venta primero.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Deseas eliminar esta venta?")
        if not confirmar:
            return

        exito, mensaje = eliminar_venta(self.id_venta_seleccionada)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_ventas()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        self.id_venta_seleccionada = None
        self.entry_fecha.delete(0, END)
        self.combo_clientes.set("")
        self.var_factura.set(0)
        self.tabla.selection_remove(self.tabla.selection())
        self.colocar_fecha_hoy()

    def colocar_fecha_hoy(self):
        hoy = date.today().strftime("%Y-%m-%d")
        self.entry_fecha.delete(0, END)
        self.entry_fecha.insert(0,hoy)