import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox

from controllers.cliente_controller import (
    agregar_cliente,
    listar_clientes,
    actualizar_cliente,
    eliminar_cliente
)


class ClienteFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.id_cliente_seleccionado = None
        self._todos_los_clientes = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_formulario()
        self.crear_buscador()
        self.crear_tabla()
        self.cargar_clientes()

    def crear_formulario(self):
        contenedor = tb.Frame(self)
        contenedor.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        contenedor.grid_columnconfigure(1, weight=1)

        tb.Label(
            contenedor,
            text="Módulo de clientes",
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, column=0, columnspan=4, sticky=W, pady=(0, 15))

        tb.Label(contenedor, text="Nombre").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.entry_nombre = tb.Entry(contenedor)
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        tb.Button(
            contenedor,
            text="Guardar",
            bootstyle="success",
            command=self.guardar_cliente
        ).grid(row=1, column=2, padx=5)

        tb.Button(
            contenedor,
            text="Actualizar",
            bootstyle="warning",
            command=self.editar_cliente
        ).grid(row=1, column=3, padx=5)

        tb.Button(
            contenedor,
            text="Limpiar",
            bootstyle="secondary",
            command=self.limpiar_formulario
        ).grid(row=1, column=4, padx=5)

    def crear_buscador(self):
        marco = tb.Frame(self)
        marco.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        marco.grid_columnconfigure(1, weight=1)
 
        tb.Label(marco, text="🔍 Buscar:").grid(row=0, column=0, sticky=W, padx=(0, 8))
 
        self.var_busqueda = tb.StringVar()
        self.var_busqueda.trace_add("write", self._filtrar)
 
        self.entry_busqueda = tb.Entry(marco, textvariable=self.var_busqueda)
        self.entry_busqueda.grid(row=0, column=1, sticky="ew", padx=(0, 8))
 
        tb.Button(
            marco,
            text="✕",
            bootstyle="secondary-outline",
            width=3,
            command=self.limpiar_busqueda
        ).grid(row=0, column=2)

    def crear_tabla(self):
        marco_tabla = tb.Frame(self)
        marco_tabla.grid(row=2, column=0, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        columnas = ("id_cliente", "nombre")

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        self.tabla.heading("id_cliente", text="ID")
        self.tabla.heading("nombre", text="Nombre")

        self.tabla.column("id_cliente", width=80, anchor=CENTER)
        self.tabla.column("nombre", width=400, anchor=CENTER)

        scrollbar = ttk.Scrollbar(marco_tabla, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        marco_tabla.grid_rowconfigure(0, weight=1)
        marco_tabla.grid_columnconfigure(0, weight=1)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

        botones = tb.Frame(self)
        botones.grid(row=3, column=0, sticky=W, pady=(10, 0))

        tb.Button(
            botones,
            text="Eliminar seleccionado",
            bootstyle="danger",
            command=self.borrar_cliente
        ).pack(side=LEFT)

    def cargar_clientes(self):
        self._todos_los_clientes = listar_clientes()
        self._actualizar_tabla(self._todos_los_clientes)
    
    def _actualizar_tabla(self, clientes):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for cliente in clientes:
            self.tabla.insert("", END, values=(cliente[0], cliente[1]))

    def _filtrar(self, *args):
        texto = self.var_busqueda.get().strip().lower()
        if not texto:
            self._actualizar_tabla(self._todos_los_clientes)
            return
        filtrados = [
            c for c in self._todos_los_clientes
            if texto in str(c[0]).lower() or texto in c[1].lower()
        ]
        self._actualizar_tabla(filtrados)

    def limpiar_busqueda(self):
        self.var_busqueda.set("")
        self.entry_busqueda.focus()

    def guardar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        exito, mensaje = agregar_cliente(nombre)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_cliente(self, event):
        item = self.tabla.selection()
        if not item:
            return

        valores = self.tabla.item(item, "values")
        self.id_cliente_seleccionado = int(valores[0])

        self.entry_nombre.delete(0, END)
        self.entry_nombre.insert(0, valores[1])

    def editar_cliente(self):
        if self.id_cliente_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un cliente primero.")
            return

        nuevo_nombre = self.entry_nombre.get().strip()
        exito, mensaje = actualizar_cliente(self.id_cliente_seleccionado, nuevo_nombre)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", mensaje)

    def borrar_cliente(self):
        if self.id_cliente_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un cliente primero.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Deseas eliminar este cliente?")
        if not confirmar:
            return

        exito, mensaje = eliminar_cliente(self.id_cliente_seleccionado)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        self.id_cliente_seleccionado = None
        self.entry_nombre.delete(0, END)
        self.tabla.selection_remove(self.tabla.selection())